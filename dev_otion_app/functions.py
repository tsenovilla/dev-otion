from uuid import uuid4

def unique_image_name (instance, filename):
    """
    This function is used by ImageField's upload_to in order to get a unique name for an updated image, obtained via uuid4. 
    WARNING: You might be tempted to use a lambda function instead of this one. That works perfectly when the application is running, but it fails when we make Django migrations. This is due to lambda functions cannot be serialized, which is a requirement for Django's migration framework. Therefore, to achieve a more consistent app, it is better to use this one.
    """
    return 'dev_otion_app/static/dev_otion_app/img/'+uuid4().hex+'.'+filename.split('.')[-1]