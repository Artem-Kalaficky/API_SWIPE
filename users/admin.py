from django.contrib import admin

from users.models import Notary, UserProfile


admin.site.register(Notary)
admin.site.register(UserProfile)
