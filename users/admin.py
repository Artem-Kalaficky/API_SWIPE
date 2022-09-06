from django.contrib import admin

from .models import Notary, UserProfile, Message, Filter


admin.site.register(Notary)
admin.site.register(UserProfile)
admin.site.register(Message)
admin.site.register(Filter)
