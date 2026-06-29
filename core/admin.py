from django.contrib import admin
from .models import UserProfile, Postage, Announcements


# Register your models here.

admin.site.register(UserProfile)

admin.site.register(Postage)

admin.site.register(Announcements)