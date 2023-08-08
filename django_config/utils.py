from uuid import uuid4
import os

def unique_filename(filename):
    _,extension = os.path.splitext(filename)
    return uuid4().hex+extension