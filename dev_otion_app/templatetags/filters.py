import os 
from django import template 

register = template.Library()

## This filter takes an image uploaded via ImageField and returns its basename.
@register.filter
def image_name(image):
    return os.path.basename(image.name)