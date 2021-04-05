"""MobileProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path("register",registration,name="register"),
    path("signin",signin,name="signin"),
    path('signout', signout, name="signout"),
    path("", HomeView.as_view(), name="home"),
    path("view/<int:pk>", MobileView.as_view(), name="view"),
    path("cart/<int:pk>", Addtocart.as_view(), name="cart"),
    path("viewcart", CartView.as_view(), name="viewcart"),
    path("manage-cart/<int:cp_id>",ManageCart.as_view(),name="managecart"),
    path("emptycart",EmptyCart.as_view(),name="emptycart"),
    path("placeorder",PlaceOrderView.as_view(),name="placeorder"),

]
