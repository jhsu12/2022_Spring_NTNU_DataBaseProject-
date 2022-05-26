from datetime import datetime
import Auctions
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from . import models

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
    global user_id
    user_name = user_is_authenticated()
   
    
    return render(request, 'HTML/index.html', {
            "user_id": user_id,
            "user_name": user_name
            
        })

def create(request):
    pass

def watchlist(request):
    pass


def logout(request):
    pass

def notification(request):
    pass