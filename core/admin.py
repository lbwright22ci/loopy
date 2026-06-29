from django.contrib import admin
from .models import UserProfile, Postage


# Register your models here.

admin.site.register(UserProfile)

admin.site.register(Postage)