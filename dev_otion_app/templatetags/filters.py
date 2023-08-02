import os 
from django import template 

register = template.Library()

@register.filter
def original_image(image):
    """This filter returns the name for an image uploaded via ImageField."""
    return os.path.basename(image.name)

@register.filter
def webp_image(image):
    """This filter returns the webp version for an image uploaded via ImageField"""
    return os.path.basename(image.name).split('.')[0]+'.webp'

@register.filter
def avif_image(image):
    """This filter returns the avif version for an image uploaded via ImageField"""
    return os.path.basename(image.name).split('.')[0]+'.avif'