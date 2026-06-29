from django.contrib import admin
from .models import (
    UserProfile, Postage, Announcements, 
    SaleSettings, ShopContactInfo, HomePageSlides )


# Register your models here.

admin.site.register(UserProfile)

admin.site.register(Postage)

admin.site.register(Announcements)

admin.site.register(SaleSettings)

admin.site.register(ShopContactInfo)

admin.site.register(HomePageSlides)