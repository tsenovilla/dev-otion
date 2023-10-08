from django.utils.translation import activate
from django.urls import reverse
from django import forms
from pathlib import Path
from uuid import uuid4
import os
import re
from PIL import Image
import pillow_avif

def unique_image_name (instance, filename:str) -> str:
    """
    This function is used by ImageField's upload_to in order to get a unique name for an updated image, obtained via uuid4. 
    WARNING: You might be tempted to use a lambda function instead of this one. That works perfectly when the application is running, but it fails when we make Django migrations. This is due to lambda functions cannot be serialized, which is a requirement for Django's migration framework. Therefore, to achieve a more consistent app, it is better to use this one.
    """
    return uuid4().hex+'.'+filename.split('.')[-1]

def reverse_self_url(dev_otion_view, *, languages: list, current_language: str, languages_slugs: dict ={}) -> dict:
    """
    This function is used to get reverse translations for the current view's url. 
    :param dev_otion_view: The view calling this function, so in general this parameter will be valued to "self".
    :param languages (kw argument): A list containing the languages where the reversion is needed. Example: spanish->"es"
    :param current_language (kw argument): The language currently selected.
    :param languages_slugs (kw argument): If the url contain a slug that changes in each language, a dict containing them as values while the keys are the languages.
    :return:  A dictionary containing the reverted urls as values. The keys will be the related languages
    """
    reverted_urls = {}
    for language in languages:
        activate(language)
        reverted_urls[language] = reverse(dev_otion_view.request.resolver_match.view_name, kwargs=dev_otion_view.request.resolver_match.kwargs) ## The kwargs must be present as some url patterns contain parameters that must be resolved during the reverse action
        try:
            reverted_urls[language] = '/'.join(reverted_urls[language].split('/')[:-1:])+'/'+languages_slugs[language] ## Dev_otion_app slugs are always at the end of the url
        except KeyError:
            pass
    activate(current_language) ## We have activated several languages in order to revert urls, so we have to reactivate the original language
    return reverted_urls

def image_improver(image: str):
    """
    This function is called when a new image is uploaded to the server in order to obtain WebP and AVIF versions for this image, improving the web performance
    :param image: The path to the uploaded image
    """
    image_path = str(Path(__file__).resolve().parent.parent) + image
    pillow_image = Image.open(image_path)
    pillow_image.save(f'{image_path.split(".")[0]}.webp', format='WEBP')
    pillow_image.save(f'{image_path.split(".")[0]}.avif', format='AVIF', codec = 'rav1e', quality = 70) 
    ## Following the recommendations from pillow_avif's creator, we set codec and quality

def delete_former_image(former_image: str):
    """
    This function is used to delete images hosted in the server which are not longer required. It deletes all existing image's versions (jpg, png, webp, avif,...)
    :param former_image: The path to the image whose versions must be deleted.
    """
    try:
        os.remove(str(Path(__file__).resolve().parent.parent)+former_image)
    except:
        pass
    try:
        os.remove((str(Path(__file__).resolve().parent.parent)+former_image).split('.')[0]+'.webp')
    except:
        pass
    try:
        os.remove((str(Path(__file__).resolve().parent.parent)+former_image).split('.')[0]+'.avif')
    except:
        pass

def create_picture_tags_CKEditor(db_entry: str, alt_text: str) -> str:
    """
    This function is used to transform the img tags created after an image upload by CKEditor into a picture tag containing AVIF, WebP and the original image tag. 
    :param db_entry: The db_entry where the image's been loaded.
    :param alt_text: The alternative text that must be shown if the image is not found.
    :return: A string containing the obtained picture tag
    """
    return re.sub('<img.*src="(?P<source>[^"]+)".*>',lambda match: f'<picture><source srcset="{match.group("source").split(".")[0]}.avif" type="image/avif"><source srcset="{match.group("source").split(".")[0]}.webp" type="image/webp"><img src="{match.group("source")}" alt="{alt_text}" loading="lazy"></picture>', db_entry)

class ContactForm(forms.Form):
    """
    This class represent form objects submitted in the contact view.
    """
    e_mail = forms.EmailField(required = True)
    message = forms.CharField(min_length = 50, required = True)