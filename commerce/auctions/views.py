from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Max
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import *
from django.contrib.auth.decorators import login_required

class NewListingForm(forms.Form):
    title = forms.CharField(widget=forms.Textarea(attrs={'class': 'title_area'}))
    image_url = forms.CharField(widget=forms.Textarea(attrs={'class': 'url_area'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'description_area'}))
    price = forms.DecimalField(label='Starting bid', widget=forms.NumberInput(attrs={'class': 'price_area'}))
    category = forms.ModelMultipleChoiceField(label='Categories', queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'select_area'}))

class NewBidForm(forms.Form):
    bid_value = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'bid_area', 'placeholder': 'Bid'}))

class NewCommentForm(forms.Form):
    topic = forms.CharField(widget=forms.Textarea(attrs={'class': 'topic_area'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'content_area'}))

def index(request):
    listings = Listing.objects.filter(closed=False)
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
    listing = Listing.objects.get(pk=listing_id)
    categories = listing.category.all()
    bids = listing.bids.all()
    temp = listing.bids.aggregate(Max('value'))
    bid = listing.bids.filter(value=temp['value__max']).first()

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "bids": bids,
        "winning": bid,
        "categories": categories,
        "bid": NewBidForm()
    })

def category(request, category_name):
    listings = Listing.objects.filter(category__name=category_name)
    return render(request, "auctions/index.html", {
        "listings": listings
    })

@login_required(login_url='login')
def watchlist(request):
    return render(request, "auctions/watchlist.html")


@login_required(login_url='login')
def createListing(request):
    return render(request, "auctions/create.html", {
        "listing": NewListingForm()
    })



