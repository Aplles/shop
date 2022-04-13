from random import randint
from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from shop.forms import *
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from .models import *


class HomePage(ListView):
    paginate_by = 12
    model = Product
    template_name = 'shop/index.html'
    context_object_name = 'produsts'
    ordering = ['id']

    def get_queryset(self):
        if self.request.GET and self.request.GET.get('orderby') != None:
            return Product.objects.filter(is_availability=True, quantity__gte=0).order_by(self.request.GET.get('orderby'))
        else:
            return Product.objects.filter(is_availability=True, quantity__gte=0)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Главная страница"
        context['name_url'] = "home"
        return context


class ProductCategory(ListView):
    model = Product
    template_name = 'shop/category.html'
    context_object_name = 'produsts'

    def get_queryset(self):
        if self.request.GET:
            return Product.objects.filter(is_availability=True, quantity__gte=0, cat__slug=self.kwargs['cat_slug']).order_by(
                self.request.GET.get('orderby'))
        else:
            return Product.objects.filter(is_availability=True, quantity__gte=0, cat__slug=self.kwargs['cat_slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Поиск по категории"
        context['cat_slug'] = self.kwargs['cat_slug']
        return context


class ResSearch(ListView):
    model = Product
    template_name = 'shop/search.html'
    context_object_name = 'produsts'

    def get_queryset(self):
        if self.request.GET and self.request.GET.get('orderby') != None:
            return Product.objects.filter(is_availability=True, quantity__gte=0, name__icontains=self.request.GET['s']).order_by(
                self.request.GET.get('orderby'))
        else:
            return Product.objects.filter(is_availability=True, quantity__gte=0, name__icontains=self.request.GET['s'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Поиск по {self.request.GET['s']}"
        context['s'] = self.request.GET['s']
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
        login(self.request, user, backend='accounts.email_backend.CustomBackend')
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
        'title': 'Оформление заказа'
    }
    return render(request, 'shop/order.html', context=context)


def add_order(request):
    count = int(request.GET.get('count'))
    d = int(request.GET.get('deliveryMethod'))
    p = int(request.GET.get('paymentMethod'))
    user = request.user
    product = Product.objects.get(slug=request.GET.get('product'))
    if count > product.quantity:
        comment = "Извините, но данного товара в таком наличии нет"
        return render(request, 'shop/error-order.html', context={'comment': comment, 'title': 'Ошибка оформления'})
    else:
        product.quantity -= count
        product.save()
        comment = 'Заказ успешно оформлен'
        order = Order(all_price=count * product.price, comment=comment, amount=count, slug=randint(1000, 99999), customer=user,
                      product=product, delivery_status=Status.objects.get(pk='1'), delivery_name=DeliveryMethod.objects.get(pk=d),
                      payment=PaymentMethod.objects.get(pk=p))
        order.save()
    return redirect('result_order')


class MyOrders(ListView):
    model = Order
    template_name = 'shop/list_orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        email = self.request.user
        user = Customer.objects.get(email=email)
        return Order.objects.filter(customer=user.pk)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Мои заказы'
        return context


def result_order(request):
    email = request.user
    user = Customer.objects.get(email=email)
    order = Order.objects.filter(customer=user.pk).last()
    return render(request, 'shop/result_order.html', context={'order': order, 'title': 'Заказ успешно оформлен'})


def delete_order(request, slug_order):
    order = Order.objects.get(slug=slug_order)
    order.delete()
    return redirect('my_orders')


def about(request):
    return render(request, 'shop/about.html', context={'title': 'О нас'})
