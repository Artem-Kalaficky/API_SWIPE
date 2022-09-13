from django.contrib import admin

from ads.models import Promotion
from users.models import Ad, Complaint, Photo


admin.site.register(Ad)
admin.site.register(Photo)
admin.site.register(Promotion)
admin.site.register(Complaint)



