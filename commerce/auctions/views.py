from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.db.models import Max
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime

class NewListingForm(forms.Form):
    title = forms.CharField(widget=forms.Textarea(attrs={'class': 'title_area'}))
    image_url = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'url_area'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'description_area'}))
    price = forms.DecimalField(label='Starting bid', min_value=0.01, widget=forms.NumberInput(attrs={'class': 'price_area'}))
    category = forms.ModelMultipleChoiceField(required=False, label='Categories', queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'select_area'}))


class NewBidForm(forms.Form):
    bid_value = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'bid_area', 'placeholder': 'Bid'}))

class NewCommentForm(forms.Form):
    topic = forms.CharField(widget=forms.Textarea(attrs={'class': 'topic_area', 'placeholder': 'Topic'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'content_area', 'placeholder': 'Content'}))

def index(request):
    listings = Listing.objects.filter(closed=False)
    
    for listing in listings:
        if not listing.bids.all():
            listing.actual_price = None

    return render(request, "auctions/index.html", {
        "listings": listings
    })

def login_view(request):

    next_page = None
    try:
        next_page = request.GET['next']
    except:
        print("next is not provided")

    if request.method == "POST":            

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            if next_page is not None:
                return HttpResponseRedirect(next_page)
            else:
                return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all()
    })

def listing(request, listing_id):
    try:
        listing = Listing.objects.get(pk=listing_id)
    except:
        return HttpResponseRedirect(reverse("error"))
    
    categories = listing.category.all()
    comments = listing.comments.all()
    bids = listing.bids.all()
    temp = listing.bids.aggregate(Max('value'))
    bid = listing.bids.filter(value=temp['value__max']).first()
    on_watchlist = False

    if request.user.is_authenticated:
        user = request.user
        watchlist = user.watchlist_listings.all()

        if listing in watchlist:
            on_watchlist = True

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "bids": bids,
        "winning": bid,
        "categories": categories,
        "comment": NewCommentForm(),
        "comments": comments,
        "on_watchlist": on_watchlist,
        "bid": NewBidForm()
    })

def category(request, category_name):
    listings = Listing.objects.filter(category__name=category_name)
    return render(request, "auctions/index.html", {
        "listings": listings
    })

def comment(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        current_user = request.user
        user = User.objects.get(pk=current_user.id)

        form = NewCommentForm(request.POST)
        if form.is_valid():
            new_comment = Comment()
            new_comment.topic = form.cleaned_data["topic"]
            new_comment.content = form.cleaned_data["content"]
            new_comment.commentator = user
            new_comment.listing = listing
            new_comment.save()

        return HttpResponseRedirect(reverse("listing", args=(listing.id,)))

def bid(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        current_user = request.user
        user = User.objects.get(pk=current_user.id)
        bids = listing.bids.all()

        if bids:
            temp = listing.bids.aggregate(Max('value'))
            bid = listing.bids.filter(value=temp['value__max']).first()
            bid_value = bid.value

        form = NewBidForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["bid_value"] < listing.price:
                messages.error(request, 'Your bid value must be at least equal to the actual price!')
            elif bids:
                if form.cleaned_data["bid_value"] <= bid_value:
                    messages.error(request, 'Your bid value must be higher than actual price!')
                else:
                    if bid.user == request.user:
                        messages.error(request, 'You cannot bid on a winning auction!')
                    else:
                        new_bid = Bid()
                        new_bid.value = form.cleaned_data["bid_value"]
                        new_bid.user = user
                        new_bid.listing = listing
                        new_bid.save()
                        listing.actual_price = form.cleaned_data["bid_value"]
                        listing.save()
            else:
                new_bid = Bid()
                new_bid.value = form.cleaned_data["bid_value"]
                new_bid.user = user
                new_bid.listing = listing
                new_bid.save()
                listing.actual_price = form.cleaned_data["bid_value"]
                listing.save()

        return HttpResponseRedirect(reverse("listing", args=(listing.id,)))

def close(request, listing_id):
    if request.user.is_authenticated:
        listing = Listing.objects.get(pk=listing_id)
        if request.user == listing.creator:
            bids = listing.bids.all()

            if bids:
                temp = listing.bids.aggregate(Max('value'))
                biggest_bid = listing.bids.filter(value=temp['value__max']).first()
                user = User.objects.get(pk=biggest_bid.user.id)
                listing.winner = user

            listing.closing_date = datetime.now()
            listing.closed = True
            listing.save()

            return HttpResponseRedirect(reverse("listing", args=(listing.id,)))
    return HttpResponseRedirect(reverse("error"))

def newListing(request):
    if request.method == "POST":
        current_user = request.user
        user = User.objects.get(pk=current_user.id)

        form = NewListingForm(request.POST)
        if form.is_valid():
            categories = form.cleaned_data["category"]

            new_listing = Listing()
            new_listing.title = form.cleaned_data["title"]
            new_listing.description = form.cleaned_data["description"]
            new_listing.price = form.cleaned_data["price"]
            new_listing.image_url = form.cleaned_data["image_url"]
            new_listing.creator = user
            new_listing.save()
            new_listing.follower.add(user)
            new_listing.save()

            for category in categories.iterator():
                new_listing.category.add(category)
            new_listing.save()
            
            return HttpResponseRedirect(reverse("listing", args=(new_listing.id,)))
        return HttpResponseRedirect(reverse("createListing"))

@login_required(login_url='login')
def watchlist(request):
    user = request.user
    listings = user.watchlist_listings.all()
    return render(request, "auctions/index.html", {
        "listings": listings,
        "watchlist": True
    })

def AddOrDelete(request, listing_id):
    if request.user.is_authenticated:
        user = request.user
        listing = Listing.objects.get(pk=listing_id)
        watchlist = user.watchlist_listings.all()

        if listing not in watchlist:
            user.watchlist_listings.add(listing)
        else:
            user.watchlist_listings.remove(listing)

        return HttpResponseRedirect(reverse("listing", args=(listing.id,)))
    return HttpResponseRedirect(reverse("error"))

@login_required(login_url='login')
def createListing(request):
    return render(request, "auctions/create.html", {
        "listing": NewListingForm()
    })

def error(request):
    return render(request, "auctions/error.html",{
        "message": "Page not found"
    })



