from django.contrib import admin

from users.models import Notary, UserProfile, Message, Filter


admin.site.register(Notary)
admin.site.register(UserProfile)
admin.site.register(Message)
admin.site.register(Filter)
