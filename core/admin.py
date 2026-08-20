from django.contrib import admin
from .models import (
    UserProfile, Postage)

# Register your models here.


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Displays instances of :model:`UserProfile` in the Django Admin panel
    List fields are 'user__first_name', 'user__last_name', 'user__email'
    Search fields are 'user__last_name', 'user__email', 'default_phone',
      'default_postcode'
    """
    list_display = ('user__first_name', 'user__last_name', 'user__email')
    search_fields = ('user__last_name', 'user__email',
                     'default_phone', 'default_postcode',)


@admin.register(Postage)
class PostageAdmin(admin.ModelAdmin):
    """
    Displays instances of :model:`Postage` in the Django Admin panel
    List fields are 'postage_class', 'parcel_size', 'postage_cost'
    """
    list_display = ('postage_class', 'parcel_size', 'postage_cost')
    list_editable = ('postage_cost',)
