from datetime import datetime
import Auctions
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from . import models

global categories
categories = ('Antiques', 'Art', 'Books', 'CDs, DVDs, Games', 'Clothing', 'Collectibles', 'Computers',
				'Dining', 'Electronics', 'Food & Gourmet Items', 'For Your Pet', 'Golf & Sports Gear',
				'Handbags', 'Health & Fitness', 'Home', 'Jewelry', 'Lawn & Garden', 'Memorabilia', 'Other',
				'Services', 'Spa & Beauty', 'Tickets-Entertainment', 'Tickets-Sports', 'Toys', 'Travel',
				'Unique Experiences', 'Wine')

global user_id
user_id = 1
def user_is_authenticated():
    global user_id
    user_name = None
    #Signed in
    if user_id != -1:
        user_data = models.SQL(f"select * from user where id = {user_id};")
        user_name = user_data[0]["username"]
    return user_name


def index(request):
    # Check whether user is login or not 
    global user_id, categories
    if user_id == -1:
        return HttpResponseRedirect(reverse("auc:login"))
    user_name = user_is_authenticated()

    if request.method == "GET":
        return render(request, 'HTML/index.html', {
                "user_id": user_id,
                "user_name": user_name,
                "categories": categories,
                
            })
    #request.method == "POST" sort by time or category


def create(request):
    if request.method == "POST":
        pass
    #else GET request

def watchlist(request):
    pass

def login(request):
    pass

def logout(request):
    pass

def notification(request):
    pass

def product(request, p_id):#p_id = product_id
    pass