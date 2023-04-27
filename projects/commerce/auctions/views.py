from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
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

class CommentForm(forms.Form):
    CommentContent = forms.CharField(label='Add comment', widget=forms.Textarea(attrs={'rows': 4}))

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
    
@login_required
def watchlist(request):
    return render(request, "auctions/watchlist.html", {
        "items": request.user.watchlist_user.all()
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

@login_required
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
    watchlist = request.user in listing.watchlist.all()
    comments = Comment.objects.filter(listing=listing)
    orig_price = Listing.objects.get(pk=listing_id).price
    highest_bid = Bid.objects.filter(listing=listing).order_by('amount').last()
    if highest_bid:
        min_value = highest_bid.amount+1
    else:
        min_value = orig_price
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "watchlist": watchlist,
        "comments": comments,
        "comment_form": CommentForm(),
        "bid_form": BidForm(min_value=min_value),
        "highest_bid": highest_bid
    })


@login_required
def add_to_watchlist(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    listing.watchlist.add(request.user)
    return HttpResponseRedirect(reverse("listing", args={listing_id, }))

@login_required
def remove_from_watchlist(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    listing.watchlist.remove(request.user)
    return HttpResponseRedirect(reverse("listing", args={listing_id, }))

@login_required
def add_comment(request, listing_id):
    if request.method == "POST":
        form = CommentForm(request.POST)
        listing = Listing.objects.get(pk=listing_id)
        if form.is_valid():
            CommentContent = form.cleaned_data["CommentContent"]

            # create new comment
            comment = Comment.objects.create(user=request.user, listing=listing, content=CommentContent, timestamp=timezone.now())
            comment.save()
    return HttpResponseRedirect(reverse("listing", args={listing_id, }))

class BidForm(forms.Form):
    def __init__(self, *args, **kwargs):
        min_value = kwargs.pop('min_value', None)
        super().__init__(*args, **kwargs)
        self.fields['BidValue'] = forms.IntegerField(
            label='Bid on this item', min_value=min_value
        )

@login_required
def bid_on_item(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        orig_price = Listing.objects.get(pk=listing_id).price
        highest_bid = Bid.objects.filter(listing=listing).order_by('amount').last()
        if highest_bid:
            min_value = highest_bid.amount+1
        else:
            min_value = orig_price
        form = BidForm(request.POST, min_value=min_value)
        if form.is_valid():
            BidValue = form.cleaned_data["BidValue"]

            # create new comment
            bid = Bid.objects.create(user=request.user, listing=listing, amount=BidValue, timestamp=timezone.now())
            bid.save()
    return HttpResponseRedirect(reverse("listing", args={listing_id, }))

@login_required
def close_auction(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    listing.isActive = False
    listing.save()
    print(f"Closing auction {listing.title}")
    return HttpResponseRedirect(reverse("listing", args={listing_id, }))