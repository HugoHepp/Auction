from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import User
import datetime
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import *



class Add_auction_form(forms.Form):

    CATEGORIES = (
    ('Electronics','Electronics'),
    ('Sport','Sport'),
    ('Mode', 'Mode'),
    ('Toys', 'Toys')
    )

    title = forms.CharField(label='Title', max_length=100)
    description = forms.CharField(label='Description', max_length=100,widget=forms.Textarea(attrs={'rows': 3,'cols': 19}))
    price = forms.DecimalField(max_digits=6, decimal_places=2, label="Price ($) ")
    category = forms.ChoiceField(choices=CATEGORIES)
    url_pic = forms.URLField()


class Bid_form(forms.Form):
    bid = forms.DecimalField(max_digits=6, decimal_places=2, label="")


class Comment_form(forms.Form):
    comment = forms.CharField(max_length=250, label="", widget=forms.Textarea(attrs={'rows': 3,'cols': 35}))




# Home page
def index(request):

    return render(request, "auctions/index.html", {"auctions": Auction.objects.all()})

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
def add_auction(request):
    if request.method == "POST":
        form = Add_auction_form(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            price = form.cleaned_data['price']
            category = form.cleaned_data['category']
            picture = form.cleaned_data['url_pic']

            data = Auction(name = title, owner = request.user, description = description, category = category, picture = picture, creationdate = datetime.datetime.now(), price = price)
            data.save()
            tmp = Auction.objects.get(name = title, owner = request.user, description = description, category = category, picture = picture)
            print(tmp.name)
            ini_bid = Bids(id_auction = tmp, current_bid = price, current_winner=request.user, date_bid = datetime.datetime.now())
            ini_bid.save()
            return HttpResponseRedirect('/')

        else:  
            return HttpResponseRedirect('/')

    else:
        add_auction_form = Add_auction_form()
        return render(request,"auctions/add_auction.html", {"add_auction_form" : add_auction_form})


def categories(request):
    return render(request,"auctions/categories.html")

def sport(request):
    title = "SPORT"
    data = Auction.objects.filter(category="Sport")
    return render(request,"auctions/quote.html",{"data":data, "title":title})

def electronics(request):
    title = "ELECTRONICS"
    data = Auction.objects.filter(category="Electronics")
    return render(request,"auctions/quote.html",{"data":data, "title":title})

def mode(request):
    title = "MODE"
    data = Auction.objects.filter(category="Mode")
    return render(request,"auctions/quote.html",{"data":data , "title":title})

def toys(request):
    title = "TOYS"
    data = Auction.objects.filter(category="Toys")
    return render(request,"auctions/quote.html",{"data":data , "title":title})

# Add an auction to the watchlist
@login_required
def addwlist(request, item):
    # get user id
    current_user = request.user
    # get auctions from this id
    item = Auction.objects.get(id=item)  
    # Create a new object Watchlist and save
    itemtoadd = Watchlist(id_user = current_user, id_auction = item)
    itemtoadd.save()
    #Return Watchlist
    data = Watchlist.objects.filter(id_user=request.user)
    return render(request,"auctions/watchlist.html",{"data":data})


@login_required
def rmvwlist(request, item):
    # Get item from db and delete it
    rmvitem = Watchlist.objects.get(id = item, id_user = request.user)
    rmvitem.delete()
    #Return Watchlist
    data = Watchlist.objects.filter(id_user=request.user)
    return render(request,"auctions/watchlist.html",{"data":data})

@login_required
def rmvwlistbyid(request, item):
    # Get item from db and delete it
    rmvitem = Watchlist.objects.get(id_auction = item, id_user = request.user)
    rmvitem.delete()
    #Return Watchlist
    data = Watchlist.objects.filter(id_user=request.user)
    return render(request,"auctions/watchlist.html",{"data":data})


@login_required
def watchlist(request):
    # Get watchlist and return it
    data = Watchlist.objects.filter(id_user=request.user)
    return render(request,"auctions/watchlist.html",{"data":data})

def listing(request, item):
    # get auction from database
    data = Auction.objects.get(id=item)
    # get price from database
    price = Bids.objects.get(id_auction=item)
    # get commentaries
    commentaries = Comment.objects.filter(id_auction=item)
    # check if user has this auction in his watchlist
    if request.user.is_authenticated:
        checkstate = False
        check = Auction.objects.get(id=item)
        watchlist = Watchlist.objects.filter(id_user=request.user)
        # set a variable that contain true or false if user has this auction in his watchlist
        for x in watchlist:
            if check.id == x.id_auction.id:
                checkstate = True
                break
            else:
                checkstate = False
        # Create forms
        bid_form = Bid_form()
        comment_form = Comment_form()
        return render(request,"auctions/listing.html",{"data":data, "watchlist":watchlist, "price": price, "bid_form":bid_form, "comment_form": comment_form, "commentaries" : commentaries, "checkstate" : checkstate})

    else:
        # Return the page without forms
        return render(request,"auctions/listing.html",{"data":data, "price": price})

@login_required
def bid(request, item):

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        bid = Bid_form(request.POST)
        # check whether it's valid:
        if bid.is_valid():
            # process the data in form.cleaned_data as required
            bidtmp = bid.cleaned_data['bid']
            # check if bid is higher than actual price
            checkprice = Auction.objects.get(id=item)
            if bidtmp > checkprice.price:
                # save new bid and price
                Bids.objects.filter(id_auction=item).update(current_bid=bidtmp, current_winner=request.user, date_bid=datetime.datetime.now())
                Auction.objects.filter(id=item).update(price=bidtmp)
        
                
            # redirect to a new URL:
            return HttpResponseRedirect('/')


@login_required
def close_auction(request, item):
    checkowner = Auction.objects.get(id=item)
    if checkowner.owner == request.user:
        Auction.objects.filter(id=item).update(isactive=False)

    return HttpResponseRedirect('/listing/'+ str(item))

@login_required
def add_comment(request, item):
    if request.method == 'POST':
        comment = Comment_form(request.POST)
        if comment.is_valid():
            comment_tmp = comment.cleaned_data['comment']
            data = Auction.objects.get(id=item)
            newcomment = Comment(id_auction = data, comment = comment_tmp, comment_date = datetime.datetime.now(), id_sender = request.user )
            newcomment.save()
       
    return HttpResponseRedirect('/listing/'+ str(item))

