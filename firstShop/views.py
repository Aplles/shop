from django.http import HttpResponseRedirect
from django.urls import reverse
from shop.urls import *


def app(request):
    return HttpResponseRedirect(reverse('home'))