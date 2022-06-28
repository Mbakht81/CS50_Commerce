
from xml.etree.ElementTree import Comment
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Bid, Category, Listing, User,Comment


def index(request):
    watchlist=None
    if request.user.is_authenticated:
        watchlist=request.user.watchlist.filter(is_active=True)
      
    return render(request, "auctions/index.html",{
        "listings":Listing.objects.filter(is_active= True),
        "watchlist": watchlist
    })


@login_required
def create_listing(request):
    if request.method == "POST":
        error = False
        error_message=""
        if request.POST["title"]=="":
            error= True
            error_message +="Title can't be blank. "
        if request.POST["description"] =="":
            error= True
            error_message+="Please add a description. "
        if request.POST["amount"]=="":
            error= True
            error_message+="Amount can't be blank. "
        
        if error:
            messages.error(request, error_message)
            return HttpResponseRedirect(reverse("createlisting") )
  
        title=    request.POST["title"]
        description=  request.POST["description"]
        amount =  int (request.POST["amount"])
        image_url =  request.POST["imageURL"]
        if request.POST["category"]=="":
            category= None
        else:
            category = Category.objects.get(pk = request.POST["category"])

        created_by = User.objects.get (pk=request.user.id)
        l = Listing.objects.create(title= title,description=description,amount = amount,
        image_url=image_url,category=category,is_active=True, created_by= created_by)
        return HttpResponseRedirect(reverse("index"))
                    
    else:
        watchlist = None
        if request.user.is_authenticated:
            watchlist = request.user.watchlist.filter(is_active=True)
            categories = Category.objects.all()
        return render(request,"auctions/new_listing.html", {
                "categories":categories,
                "watchlist":watchlist

            })


def categories(request):
    watchlist = None
    if request.user.is_authenticated:
        watchlist = request.user.watchlist.filter(is_active=True)
    return render(request, "auctions/categories.html",{
        "categories":Category.objects.all(),
         "watchlist":watchlist

    })

def list_by_category(request, category_id):    
    watchlist = None
    if request.user.is_authenticated:
        watchlist = request.user.watchlist.filter(is_active=True)
    return render(request, "auctions/index.html",{
        "listings":Listing.objects.filter(category= Category.objects.get(pk =category_id ), is_active=True),
        "watchlist":watchlist
    })

def close_listing(request, listing_id):
    listing = Listing.objects.get(pk =listing_id)
    listing.is_active = False
    listing.save()
    return HttpResponseRedirect(reverse("listing" , args=(listing_id,)))

def listing(request,listing_id,biderror=False):
    watchlist = None
    if request.user.is_authenticated:
        watchlist = request.user.watchlist.filter(is_active=True)
    
    listing = Listing.objects.get(pk=listing_id)
    is_watchlist = False
    if request.user in listing.prospects.all():
        is_watchlist = True

    comments = listing.comments.order_by("-id")
    bids = listing.bids.order_by("-id")
    return render(request,"auctions/listing.html",{
        "listing":listing, 
       # "is_watchlist":is_watchlist,
        "watchlist":watchlist,
        "comments":comments,
        "bids":bids,
        "biderror":biderror
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
def watchlist(request):
    watchlist = request.user.watchlist.filter(is_active =True)
    return render(request, "auctions/index.html",{
        "listings":watchlist ,
        "watchlist":watchlist
    })


@login_required
def update_watchlist(request,listing_id):
    if request.method =="POST":
        is_watchlist = False
        l = Listing.objects.get(pk = listing_id)

        if "add_watchlist" in request.POST.keys() :
            request.user.watchlist.add(l)
        else:
            request.user.watchlist.remove(l)
  
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)) )
        
@login_required
def place_bid(request,listing_id):
    if request.method =="POST":
        if request.POST["bid_amount"].strip()=="":
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

        bid_error = False
        l = Listing.objects.get(pk =listing_id)
        latest_bid_amount=0
        all_bids=l.bids.all()
        if all_bids.count() >0:
            latest_bid= l.bids.order_by("-created_date")[:1]
#            return render (request, "auctions/error.html",{
#                   "message":latest_bid[0].amount
#        })
            latest_bid_amount = int(latest_bid[0].amount)
            
        if int(request.POST["bid_amount"])> l.amount  and int(request.POST["bid_amount"])> latest_bid_amount :
            bid = Bid.objects.create(user = request.user, listing = l, amount = int(request.POST["bid_amount"]))


        else:
            bid_error=True            

        if bid_error:
            
            return listing(request,listing_id, bid_error)
        else:

            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
    else:
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

@login_required
def add_comment(request,listing_id):
    if request.method =="POST":
        if request.POST["text"].strip() != "":
            comment = Comment.objects.create(user = request.user, listing = Listing.objects.get(pk =listing_id), text = request.POST["text"])

        return HttpResponseRedirect(reverse("listing" , args=(listing_id,)))
    else:
        return render (request, "auctions/error.html",{
                "message":" not post"
            }) 

