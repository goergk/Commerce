from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import User

CATEGORIES = [
    ('toy', 'Toys'),
    ('cloth', 'Clothes'),
    ('electronic', 'Electronics'),
    ('fashion', 'Fashion'),
    ('sport', 'Sport'),
    ('book', 'Books')
]

class NewListingForm(forms.Form):
    title = forms.CharField(widget=forms.Textarea(attrs={'class': 'title_area'}))
    image_url = forms.CharField(widget=forms.Textarea(attrs={'class': 'url_area'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'description_area'}))
    price = forms.DecimalField(widget=forms.Textarea(attrs={'class': 'price_area'}))
    category = forms.CharField(widget=forms.Select(choices=CATEGORIES, attrs={'class': 'select_area'}))

def index(request):
    return render(request, "auctions/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
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
    pass

def watchlist(request):
    pass

def createListing(request):
    return render(request, "auctions/create.html", {
        "listing": NewListingForm()
    })

