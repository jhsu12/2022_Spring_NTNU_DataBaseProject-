from datetime import datetime
import Auctions
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from . import models
from datetime import datetime

global categories
categories = ('Antiques', 'Art', 'Books', 'CDs,DVDs,Games', 'Clothing', 'Collectibles', 'Computers',
				'Dining', 'Electronics', 'Food&Gourmet Items', 'ForYourPet', 'Golf&Sports Gear',
				'Handbags', 'Health&Fitness', 'Home', 'Jewelry', 'Lawn&Garden', 'Memorabilia', 'Other',
				'Services', 'Spa&Beauty', 'Tickets-Entertainment', 'Tickets-Sports', 'Toys', 'Travel',
				'UniqueExperiences', 'Wine')

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

def get_products(user_id, category, time):
    
    #products = models.SQL(f"select * from product where user_id = {user_id} and curdate() between start_time and end_time;")
    if category is None: #list all products
        if time == 'Latest':
            products = models.SQL(f"select * from product where user_id = {user_id} and curdate() between start_time and end_time order by start_time DESC;")
        else:
            products = models.SQL(f"select * from product where user_id = {user_id} and curdate() between start_time and end_time order by start_time ASC;")
    else: #list specific category
        if time == 'Latest':
            products = models.SQL(f"select * from product where user_id = {user_id} and category = '{category}' and curdate() between start_time and end_time order by start_time DESC;")
        else:
            products = models.SQL(f"select * from product where user_id = {user_id} and category = '{category}' and curdate() between start_time and end_time order by start_time ASC;")
    
    return products

def index(request):
    # Check whether user is login or not 
    global user_id, categories
    if user_id == -1:
        return HttpResponseRedirect(reverse("auc:login"))
    user_name = user_is_authenticated()

    if request.method == "GET":
        category = request.GET.get('category', None)
        time = request.GET.get('time', 'Latest')
        products = get_products(user_id, category, time)
       
        print(products)
        return render(request, 'HTML/index.html', {
                "user_id": user_id,
                "user_name": user_name,
                "categories": categories,
                "products": products,
                
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