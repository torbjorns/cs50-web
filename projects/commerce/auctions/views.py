from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Listing, Bid, Comment, Category

class NewListingForm(forms.Form):
    categories = Category.objects.all()

    listingCategories = list()

    for category in categories:
        listingCategories.append((category.categoryName, category.categoryName))

    ListingTitle = forms.CharField(label="Title")
    ListingDescription = forms.CharField(label="Description")
    ListingBid = forms.IntegerField(label="StartingBid")
    ListingImageUrl = forms.CharField(label="Image URL")
    ListingCategory = forms.ChoiceField(choices=listingCategories, label="Category")

def index(request):
    if request.method == "GET" or request.POST.get('category') == "All":
        return render(request, "auctions/index.html", {
            "items": Listing.objects.filter(isActive=True),
            "categories": Category.objects.all(),
            "active_category": None
        })
    else:
        category_name = request.POST.get('category')
        category = Category.objects.get(categoryName=category_name)
        return render(request, "auctions/index.html", {
            "items": Listing.objects.filter(isActive=True, category=category),
            "categories": Category.objects.all(),
            "active_category": category
        })

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


def new_listing(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():
            ListingTitle = form.cleaned_data["ListingTitle"]
            ListingDescription = form.cleaned_data["ListingDescription"]
            ListingBid = form.cleaned_data["ListingBid"]
            ListingImageUrl = form.cleaned_data["ListingImageUrl"]
            ListingCategory = Category.objects.get(categoryName=form.cleaned_data["ListingCategory"])

            # Attempt to create new listing
            listing = Listing.objects.create(title=ListingTitle, description=ListingDescription, price=ListingBid, imageUrl=ListingImageUrl, category=ListingCategory, owner=request.user)
            listing.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/new_listing.html", {
                'form': NewListingForm()
            })

    else:
        return render(request, "auctions/new_listing.html", {
            'form': NewListingForm()
        })

def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    try:
        watchlist = request.user.watchlist.all()
    except:
        watchlist = {}
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "watchlist": watchlist
    })

def add_to_watchlist(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    request.user.watchlist.add(listing)
    return HttpResponseRedirect(reverse("listing", args={listing_id,}))

def remove_from_watchlist(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    request.user.watchlist.remove(listing)
    return HttpResponseRedirect(reverse("listing", args={listing_id,}))