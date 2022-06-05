from datetime import datetime
import Auctions
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from . import models
from datetime import datetime

global categories
categories = ('Antiques', 'Art', 'Books', 'CDs, DVDs, Games', 'Clothing', 'Collectibles', 'Computers',
				'Dining', 'Electronics', 'Food and Gourmet Items', 'For Your Pet', 'Golf and SportsGear',
				'Handbags', 'Health and Fitness', 'Home', 'Jewelry', 'Lawn and Garden', 'Memorabilia', 'Other',
				'Services', 'Spa and Beauty', 'Tickets-Entertainment', 'Tickets-Sports', 'Toys', 'Travel',
				'Unique Experiences', 'Wine')

global user_id
user_id = 2
def user_is_authenticated():
    global user_id
    user_name = None
    #Signed in
    if user_id != -1:
        user_data = models.SQL(f"select * from user where id = {user_id};")
        user_name = user_data[0]["username"]
    return user_name

# For index page(HOME)
def get_products(category, time):
    
    if category is None: #list all products
        if time == 'Latest':
            products = models.SQL(f"select * from product where curdate() between start_time and end_time order by start_time DESC;")
        else:
            products = models.SQL(f"select * from product where curdate() between start_time and end_time order by start_time ASC;")
    else: #list specific category
        if time == 'Latest':
            products = models.SQL(f"select * from product where category = '{category}' and curdate() between start_time and end_time order by start_time DESC;")
        else:
            products = models.SQL(f"select * from product where category = '{category}' and curdate() between start_time and end_time order by start_time ASC;")
    
    return products

# For Listing page(WATCHLIST)
def get_listing_products(user_id, listing , state, category, time):

    if listing == 'WatchList':
        #natural join Product & Watchlist
        if state == 'On-Going':
            if category is None: #list all products
                if time == 'Latest':
                    products = models.SQL(f"select * from product inner join watchlist using(product_id) where watchlist.user_id = {user_id} and curdate() between start_time and end_time order by start_time DESC;")
                    print("innn")
                else:
                    products = models.SQL(f"select * from product inner join watchlist using(product_id) where watchlist.user_id = {user_id} and curdate() between start_time and end_time order by start_time ASC;")
            else: #list specific category
                if time == 'Latest':
                    products = models.SQL(f"select * from product inner join watchlist using(product_id) where watchlist.user_id = {user_id} and category = '{category}' and curdate() between start_time and end_time order by start_time DESC;")
                else:
                    products = models.SQL(f"select * from product inner join watchlist using(product_id) where watchlist.user_id = {user_id} and category = '{category}' and curdate() between start_time and end_time order by start_time ASC;")
        else:#state = End
            if category is None: #list all products
                if time == 'Latest':
                    products = models.SQL(f"select * from product inner join watchlist using(product_id) where watchlist.user_id = {user_id} and curdate() > end_time order by start_time DESC;")
                else:
                    products = models.SQL(f"select * from product inner join watchlist using(product_id) where watchlist.user_id = {user_id} and curdate() > end_time order by start_time ASC;")
            else: #list specific category
                if time == 'Latest':
                    products = models.SQL(f"select * from product inner join watchlist using(product_id) where watchlist.user_id = {user_id} and category = '{category}' and curdate() > end_time order by start_time DESC;")
                else:
                    products = models.SQL(f"select * from product inner join watchlist using(product_id) where watchlist.user_id = {user_id} and category = '{category}' and curdate() > end_time order by start_time ASC;")
        
    elif listing == 'Winning':
        #natural join Product & Winner
        if category is None: #list all products
            if time == 'Latest':
                products = models.SQL(f"select * from product inner join winner using(product_id) where winner.user_id = {user_id} order by start_time DESC;")
            else:
                products = models.SQL(f"select * from product inner join winner using(product_id) where winner.user_id = {user_id} order by start_time ASC;")
        else: #list specific category
            if time == 'Latest':
                products = models.SQL(f"select * from product inner join winner using(product_id) where winner.user_id = {user_id} and category = '{category}' order by start_time DESC;")
            else:
                products = models.SQL(f"select * from product inner join winner using(product_id) where winner.user_id = {user_id} and category = '{category}' order by start_time ASC;")
    elif listing == 'Creation':
        if state == 'On-Going':
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
        else:#state = End
            if category is None: #list all products
                if time == 'Latest':
                    products = models.SQL(f"select * from product where user_id = {user_id} and curdate() > end_time order by start_time DESC;")
                else:
                    products = models.SQL(f"select * from product where user_id = {user_id} and curdate() > end_time order by start_time ASC;")
            else: #list specific category
                if time == 'Latest':
                    products = models.SQL(f"select * from product where user_id = {user_id} and category = '{category}' and curdate() > end_time order by start_time DESC;")
                else:
                    products = models.SQL(f"select * from product where user_id = {user_id} and category = '{category}' and curdate() > end_time order by start_time ASC;")
    
    return products
def index(request):
    # Check whether user is login or not 
    global user_id, categories
    if user_id == -1:
        return HttpResponseRedirect(reverse("auc:login"))
    user_name = user_is_authenticated()

    if request.method == "GET":
        category = request.GET.get('category', None)
        if category is not None:
            category = category.replace('_', ' ').replace('and', '&');
        time = request.GET.get('time', 'Latest')
        products = get_products(category, time)
       
        #print(category)
        #print(len(products))
        return render(request, 'HTML/index.html', {
                "user_id": user_id,
                "user_name": user_name,
                "categories": categories,
                "products": products,
                "total_items": len(products),
                
            })
    


def create(request):
    # Check whether user is login or not 
    global user_id, categories
    if user_id == -1:
        return HttpResponseRedirect(reverse("auc:login"))
    user_name = user_is_authenticated()

    #title error & start_price error
    title_e = False
    start_price_e = False
    if request.method == "GET":
        return render(request, 'HTML/CreateListing.html', {
                "user_id": user_id,
                "user_name": user_name,
                "categories": categories,
                "title_e": title_e,
                "start_price_e": start_price_e,
            })
    elif request.method == "POST":
        #Get data and check
        #if not valid show error message & auto-fill the form?
        Title = request.POST["title"]
        Start_Date = request.POST["start_date"]
        End_Date = request.POST["end_date"]
        Category = request.POST["category"].replace('and', '&');
        Start_Price = request.POST["start_price"]
        Image = request.POST["image"]
        Description = request.POST["description"]

        if(not(Title and Title.strip())):
            title_e = True
        if(int(Start_Price) < 0 ):
            start_price_e = True
        
        if(title_e or start_price_e):
            return render(request, 'HTML/CreateListing.html', {
                "user_id": user_id,
                "user_name": user_name,
                "categories": categories,
                "title_e": title_e,
                "start_price_e": start_price_e,
            })
        sm, sd, sy = Start_Date.split('/')
        em, ed, ey = End_Date.split('/')
        Start_Date = f"{sy}-{sm}-{sd}"
        End_Date = f"{ey}-{em}-{ed}"

        # insert tuple to product
        models.SQL(f"insert into product (user_id, name, description, category, image, start_time, end_time, start_price) values ('{user_id}', '{Title}', '{Description}', '{Category}', '{Image}', '{Start_Date}', '{End_Date}', {Start_Price});")
        #print(Title, Start_Date, End_Date, Category, Start_Price, Image, Description)
        return HttpResponseRedirect(reverse("auc:index"))
        

def watchlist(request):
    # Check whether user is login or not 
    global user_id, categories
    if user_id == -1:
        return HttpResponseRedirect(reverse("auc:login"))
    user_name = user_is_authenticated()

    if request.method == "GET":
        winning = False

        listing = request.GET.get('listing', 'WatchList')
        state = request.GET.get('state', 'On-Going')
        category = request.GET.get('category', None)
        time = request.GET.get('time', 'Latest')

        if category is not None:
            category = category.replace('_', ' ').replace('and', '&')
        if listing == 'Winning':
            winning = True
        #products = get_products(category, time)
        #print(listing, state, category, time)
        products = get_listing_products(user_id, listing, state, category, time)
        #print(products)
        #print(category)
        #print(len(products))
        return render(request, 'HTML/Listing.html', {
                "user_id": user_id,
                "user_name": user_name,
                "categories": categories,
                "winning": winning,
                "products": products,
                "total_items": len(products),
                
            })

def login(request):
    pass

def logout(request):
    pass

def notification(request):
    pass

def product(request, p_id):#p_id = product_id
    pass