from random import randint

from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView

from shop.forms import *
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from .models import *


class HomePage(ListView):
    model = Product
    template_name = 'shop/index.html'
    context_object_name = 'produsts'

    def get_queryset(self):
        return Product.objects.filter(is_availability=True, quantity__gt=0)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Главная страница"
        return context


class ProductCategory(ListView):
    model = Product
    template_name = 'shop/category.html'
    context_object_name = 'produsts'

    def get_queryset(self):
        return Product.objects.filter(is_availability=True, quantity__gt=0, cat__slug=self.kwargs['cat_slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Категория"
        return context


class ResSearch(ListView):
    model = Product
    template_name = 'shop/search.html'
    context_object_name = 'produsts'

    def get_queryset(self):
        return Product.objects.filter(is_availability=True, quantity__gt=0, name__contains=self.request.GET['s'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Поиск по {self.request.GET['s']}"
        return context


class RegisterUser(CreateView):
    form_class = CustomRegisterForm
    template_name = 'shop/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Регистрация"
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'shop/login.html'

    def get_success_url(self):
        return reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Авторизация"
        return context


def logout_user(request):
    logout(request)
    return redirect('home')


def new_order(request, product_slug):
    product = Product.objects.get(slug=product_slug)
    form = InfoProductForm()
    context = {
        'product': product,
        'form': form,
    }
    return render(request, 'shop/order.html', context=context)


def add_order(request):
    count = int(request.GET.get('count'))
    d = int(request.GET.get('deliveryMethod'))
    p = int(request.GET.get('paymentMethod'))
    comment = str(request.GET.get('comment'))
    if len(comment) == 0:
        comment = "Комментарий отсутствует"
    user = request.user
    product = Product.objects.get(slug=request.GET.get('product'))

    order = Order(all_price=count * product.price, comment=comment, amount=count, slug=randint(1000, 99999), customer=user,
                  product=product, delivery_status=Status.objects.get(pk='1'), delivery_name=DeliveryMethod.objects.get(pk=d),
                  payment=PaymentMethod.objects.get(pk=p))
    order.save()
    return render(request, 'shop/result_order.html')


class MyOrders(ListView):
    model = Order
    template_name = 'shop/list_orders.html'

    def get_queryset(self):
        # user = Customer.objects.get(email=)
        return Order.objects.all()
