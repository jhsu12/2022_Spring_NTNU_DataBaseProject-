from django.urls import path

from . import views
app_name = "auc"
urlpatterns = [
    path('', views.login, name='index'),#HOME
    path('create', views.create, name='create'),
    path('watchlist', views.watchlist, name='watchlist'),

    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),

    path('notification', views.notification, name='notification'),
    path('product/<int:p_id>', views.product, name='product'),
]