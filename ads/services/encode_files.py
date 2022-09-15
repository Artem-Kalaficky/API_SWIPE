import base64
from django.core.files.base import ContentFile
from users.models import Photo, Ad


def generate_base64():
    with open('ads/static/ads/images/house.jpg', 'rb') as img_file:
        my_string = base64.b64encode(img_file.read())
    return my_string

# data = ContentFile(base64.b64decode(my_string), name='house.jpg')


