from datetime import *
import Auctions
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from . import models
from datetime import datetime
from random import randrange

global categories
categories = ('Antiques', 'Art', 'Books', 'CDs, DVDs, Games', 'Clothing', 'Collectibles', 'Computers',
				'Dining', 'Electronics', 'Food and Gourmet Items', 'For Your Pet', 'Golf and SportsGear',
				'Handbags', 'Health and Fitness', 'Home', 'Jewelry', 'Lawn and Garden', 'Memorabilia', 'Other',
				'Services', 'Spa and Beauty', 'Tickets-Entertainment', 'Tickets-Sports', 'Toys', 'Travel',
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

# For checking winner
def check_winner():
    # query today > end time 's products
    end_products = models.SQL('select * from product where curdate() > end_time;')
    #print(end_products)
    # if the product current price == -1 or is already in the winner list then delete from end_products
    for p in end_products:
        
        winner = models.SQL(f'select * from winner where product_id = {p["product_id"]};')
        #print(winner, len(winner))
        if p["current_price"] == -1 or len(winner) != 0:
            # remove p from end_products
            end_products.remove(p)
        else:
            # get the winner's user_id
            winner_id = models.SQL(f'select user_id from Bid_record where product_id = {p["product_id"]} order by date_time DESC;')[0]['user_id']
            # insert new data to Winner table
            models.SQL(f'insert into Winner values ({winner_id}, {p["product_id"]});')

    
def index(request):
    # Check whether user is login or not 
    global user_id, categories
    if user_id == -1:
        return HttpResponseRedirect(reverse("auc:login"))
    user_name = user_is_authenticated()

    check_winner()
    if request.method == "GET":
        category = request.GET.get('category', None)
        if category is not None:
            category = category.replace('_', ' ').replace('and', '&');
        time = request.GET.get('time', 'Latest')
        products = get_products(category, time)

        #print(products)
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
    # Check whether user is login or not 
    global user_id, categories
    if user_id == -1:
        return HttpResponseRedirect(reverse("auc:login"))
    user_name = user_is_authenticated()

    #Get product
    product_info = models.SQL(f"select * from product where product_id = {p_id};")
    product = product_info[0]
    end_time = product["end_time"]

    invalid_bid = False
    in_watchlist = False

    if request.method == "POST":
        if request.POST['action'] == "Bid":
            try:
                new_bid = int(request.POST['value'])
            except:
                invalid_bid = True
                
            #Check whether value is valid
            if(not invalid_bid and new_bid > product['current_price'] and new_bid > product['start_price'] ):
                #new bid value
                # update Product's current_price
                models.SQL(f"update Product set current_price = {new_bid} where product_id = {p_id};")
                # insert new record in Bid_record.
                models.SQL(f"insert into Bid_Record (user_id, product_id, bid_price) values ({user_id}, {p_id}, {new_bid});")
                # query product again for latest information
                product = models.SQL(f"select * from product where product_id = {p_id};")[0]
            else:
                # invalid value, show error message
                invalid_bid = True
        elif request.POST['action'] == "Add":
            #insert data to watchlist
            models.SQL(f"insert into Watchlist (user_id, product_id) values ({user_id}, {p_id});")
        elif request.POST['action'] == "Remove":
            #delete data from watchlist
            models.SQL(f"delete from Watchlist where user_id={user_id} and product_id={p_id};")
        elif request.POST['action'] == "Comment":
            #insert into comment
            comment = request.POST['comment']
            comment = comment.replace('"', '""')
            comment = comment.replace("'", "''")
            print(comment)
            models.SQL(f"insert into Comments (user_id, product_id, comment) values ({user_id}, {p_id}, '{comment}')")
            
    #get comments
    comments = models.SQL(f"select * from Comments inner join User on User.id = Comments.user_id where Comments.product_id = {p_id};")
    #replace back in comments
    for comment in comments:
        comment['comment'] = comment['comment'].replace('""', '"')
    
    #print(date.today() > end_time)
    current_buyer = "None"

    #check current price
    if product['current_price'] != -1:
        current_buyer_id = models.SQL(f"select user_id from Bid_record where product_id = {p_id} order by date_time DESC;")[0]['user_id']
        current_buyer = models.SQL(f"select username from User where id={current_buyer_id};")[0]['username']

    #get created by's name
    created_by_id = models.SQL(f"select user_id from product where product_id = {p_id};")[0]['user_id']
    created_by = models.SQL(f"select username from User where id={created_by_id};")[0]['username']

    #check watchlist button when current user isn't the creator of the product
    if created_by_id != user_id:
        info = models.SQL(f"select * from watchlist where user_id={user_id} and product_id={p_id};")
        #print(info)
        if len(info) != 0:
            in_watchlist = True
    # get more products
    more_products = models.SQL(f'select * from product where product_id <> {p_id} and curdate() between start_time and end_time;')

    if len(more_products) > 4:
        get_f = []
        l = len(more_products)
        for i in range(4):
            ind = randrange(0, l)
            get_f.append(more_products[ind])
            more_products.remove(more_products[ind])
            l -= 1
        more_products = get_f

    return render(request, 'HTML/Product.html', {
            "user_id": user_id,
            "user_name": user_name,

            "current_buyer": current_buyer,
            "created_by": created_by,
            "valid": (date.today() < end_time and created_by_id != user_id),
            "invalid_bid": invalid_bid,
            "in_watchlist": in_watchlist,
            "created_by_current_user": (created_by_id == user_id),

            "more_products": more_products,
            "product": product,
            "total_comments": len(comments),
            "comments": comments,
            
            
        })
    


