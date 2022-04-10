from django import template
from shop.models import *

register = template.Library()


@register.filter(name='split')
def split(string: str):
    return string.split()


@register.simple_tag()
def get_categories():
    return Category.objects.all()


@register.simple_tag()
def get_models():
    return Product.objects.all().values('model')
