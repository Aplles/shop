from django.urls import path
from .views import *

urlpatterns = [
    path('', HomePage.as_view(), name='home'),  # роут главной страницы
    path('search/', ResSearch.as_view(), name='search'),  # роут для результата поиска
    path('category/<slug:cat_slug>/', ProductCategory.as_view(), name='category'),  # роут для отображения категорий
    path('register/', RegisterUser.as_view(), name='register'),  # роут для регистрации
    path('logout/', logout_user, name='logout'),  # роут выхода из аккаунта
    path('login/', LoginUser.as_view(), name='login'),  # роут авторизации
    path('order/<slug:product_slug>', new_order, name='order'),  # роут для заказа
    path('add_order/', add_order, name='new_order'),  # роут для добавления заказа
    path('my_orders/', MyOrders.as_view(), name='my_orders'),  # роут для отображения заказов определённого аккаунта
    path('result_order/', result_order, name='result_order'),  # роут для отображения страницы об успешном заказе
    path('delete_order/<slug:slug_order>', delete_order, name='del_order'),  # роут для удаления заказа :(
    path('about/', about, name='about'),  # роут для вывода инф о создателях
    path('product_info/<slug:product_slug>', ProductInfo.as_view(), name='product-info'),  # роут для вывода инф о создателях
]
