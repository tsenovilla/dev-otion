import os 
from django import template 

register = template.Library()

@register.filter
def webp_image(image):
    """This filter returns the webp version for an image uploaded via ImageField"""
    return image.url.split('.')[0]+'.webp'

@register.filter
def avif_image(image):
    """This filter returns the avif version for an image uploaded via ImageField"""
    return image.url.split('.')[0]+'.avif'

@register.filter
def get_dict_item(dictionary, key):
    """
    This filter is used to choose an item in a dictionary from a Django template.
    - INPUTS: 
        - dictionary: <class 'dict'> The dictionary where we look up
        - key: The key used to search
    - OUTPUT:
        - The desired item from the dictionary
    """
    return dictionary.get(key)