from django.utils.translation import activate
from django.urls import reverse
from pathlib import Path
from uuid import uuid4
import os
from PIL import Image
import pillow_avif

def unique_image_name (instance, filename):
    """
    This function is used by ImageField's upload_to in order to get a unique name for an updated image, obtained via uuid4. 
    WARNING: You might be tempted to use a lambda function instead of this one. That works perfectly when the application is running, but it fails when we make Django migrations. This is due to lambda functions cannot be serialized, which is a requirement for Django's migration framework. Therefore, to achieve a more consistent app, it is better to use this one.
    """
    return uuid4().hex+'.'+filename.split('.')[-1]

def reverse_self_url(dev_otion_view, *, languages, current_language, languages_slugs={}):
    """
    This function is used to get reverse translations for the current view's url. 
    - INPUTS:
        - dev_otion_view: <class 'Dev_otion_View'> The view calling this function, so in general this parameter will be valued to "self".
        - languages (kw argument): <class 'list'> A list containing the languages where the reversion is needed. Example: spanish->"es"
        - languages_slugs (kw argument): <class 'dict'> If the url contain a slug that changes in each language, a dict containing them as values while the keys are the languages.
        - current_language (kw argument): <class 'str'> The language currently selected.
    - OUTPUT: <class 'dict'> A dictionary containing the reverted urls as values. The keys will be the related language 
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

def image_improver(image):
    """
    This function is called when a new image is uploaded to the server in order to obtain WebP and AVIF versions for this image, improving the web performance
    :parm image: Recently uploaded image
    """
    image_path = str(Path(__file__).resolve().parent.parent) + image
    pillow_image = Image.open(image_path)
    pillow_image.save(f'{image_path.split(".")[0]}.webp', format='WEBP')
    pillow_image.save(f'{image_path.split(".")[0]}.avif', format='AVIF', codec = 'rav1e', quality = 70) 
    ## Following the recommendations from pillow_avif's creator, we set codec and quality

def delete_former_image(former_image):
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