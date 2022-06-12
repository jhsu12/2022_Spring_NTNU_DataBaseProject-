from datetime import datetime
import Auctions
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from . import models
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm

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
        if category is not None:
            category = category.replace('_', ' ').replace('and', '&');
        time = request.GET.get('time', 'Latest')
        products = get_products(user_id, category, time)
       
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
    pass

def logout(request):
    pass

def notification(request):
    pass

def product(request, p_id):#p_id = product_id
    pass

def login(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')  #重新導向到登入畫面
    context = {
        'form': form
    }
    return render(request, 'HTML/Login.html', context)