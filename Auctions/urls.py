from django.urls import path

from . import views
app_name = "auc"
urlpatterns = [
    path('', views.index, name='index'),#HOME
    path('create', views.create, name='create'),
    path('watchlist', views.watchlist, name='watchlist'),
    path('logout', views.logout, name='logout'),
    path('notification', views.notification, name='notification'),
]