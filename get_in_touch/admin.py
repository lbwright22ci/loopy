from django.contrib import admin
from .models import Contact

# Register your models here.

@admin.action(description="mark messages as read")
def mark_read(modeladmin, request, queryset):
    """ """
    queryset.update(read=True)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """ """
    list_display=('created_on', 'name', 'subject')
    list_filter=('read',)
    actions=[mark_read]
    search_fields=['email', 'name',]
    

