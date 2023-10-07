import json
from dev_otion_app.models import CKEditorEntryImages

## This middleware saves in the database CKEditorEntryImages all the images loaded by CKEditor. Thus, we always have control of how many images have been loaded on the server. The Entry model register in the CKEditorEntryImages db the images related to a saved Entry, and deletes all images not being used by any entry, then cleaning the server :)
class CKEditorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_superuser and request.method == 'POST' and '/ckeditor/upload/' in request.path:
            try: 
                db_image_recorder = CKEditorEntryImages()
                db_image_recorder.name = json.loads(response.content)['fileName']
                db_image_recorder.save()
            except KeyError: ## If there's a key error, it means the upload didn't go well, so we do nothing
                pass
        return response
    