from django.contrib import admin

from .models import Advantage, News, Document, Image
from users.models import House


admin.site.register(House)
admin.site.register(Advantage)
admin.site.register(News)
admin.site.register(Document)
admin.site.register(Image)
