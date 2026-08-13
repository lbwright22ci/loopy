from django.contrib import admin
from .models import Contact

# Register your models here.

@admin.action(description="Mark as read")
def mark_read(modeladmin, request, queryset):
    """ Bulk action to mark messages as read from Admin panel"""
    queryset.update(read=True)

@admin.action(description="Mark as unread")
def mark_unread(modeladmin, request, queryset):
    """ Bulk action to mark messages as unread from Admin panel"""
    queryset.update(read=False)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """ Displays instances of :model:`Contact` in the Django admin panel for editing, crreating new and updating.
    
    Fields in list display are: 'created_on', 'name', 'subject', 'read'
    Instances can be filtered by 'read' status
    Instances can be searched by 'email' and 'name'

    Instances can be updated in bulk to mark them as read.
    """
    list_display=('created_on', 'name', 'subject', 'read',)
    list_filter=('read',)
    actions=[mark_read, mark_unread]
    search_fields=['email', 'name',]