from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import *
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = Customer
        fields = ('email',)


class CustomRegisterForm(UserCreationForm):
    username = forms.CharField(label='Имя', max_length=255, widget=forms.TextInput(attrs={'id': 'textArea'}))
    email = forms.CharField(label='Почта', max_length=255, widget=forms.TextInput(attrs={'id': 'textArea'}))
    password1 = forms.CharField(label='Пароль', required=False,
                                widget=forms.PasswordInput(attrs={"cols": 40, "rows": 6, 'id': 'textArea'}))
    password2 = forms.CharField(label='Повтор пароля', required=False,
                                widget=forms.PasswordInput(attrs={"cols": 40, "rows": 6, 'id': 'textArea'}))
    contact = forms.CharField(label='Контакт', max_length=255, widget=forms.TextInput(attrs={'id': 'textArea'}))

    class Meta:
        model = User
        fields = ("username", 'email', 'password1', 'password2', 'contact')
        widgets = {
            'email': forms.TextInput(attrs={'class': 'forms'})
        }


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Почта', max_length=255, widget=forms.TextInput(attrs={'id': 'textArea'}))
    password = forms.CharField(label='Пароль', required=False,
                               widget=forms.PasswordInput(attrs={"cols": 40, "rows": 6, 'id': 'textArea'}))


class InfoProductForm(forms.Form):
    deliveryMethod = forms.ModelChoiceField(queryset=DeliveryMethod.objects.all(), label='Способ доставки', empty_label='Выберите способ доставки',
                                            widget=forms.Select(attrs={'class': 'choice'}))
    paymentMethod = forms.ModelChoiceField(queryset=PaymentMethod.objects.all(), empty_label='Выберете способ оплаты', label='Способ оплаты',
                                           widget=forms.Select(attrs={'class': 'choice'}))
