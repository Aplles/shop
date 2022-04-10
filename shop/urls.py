from django.urls import path
from .views import *

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('search/', ResSearch.as_view(), name='search'),
    path('category/<slug:cat_slug>/', ProductCategory.as_view(), name='category'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('logout/', logout_user, name='logout'),
    path('login/', LoginUser.as_view(), name='login'),
    path('order/<slug:product_slug>', new_order, name='order'),
    path('add_order/', add_order, name='new_order'),
    path('my_orders/', MyOrders.as_view(), name='my_orders'),
]

# KaraMax223
