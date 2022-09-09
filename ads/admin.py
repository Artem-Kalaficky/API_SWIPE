from django.contrib import admin

from ads.models import Promotion
from users.models import Ad


admin.site.register(Ad)
admin.site.register(Promotion)


