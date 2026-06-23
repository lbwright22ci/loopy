from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class UserProfile(models.Model):
    """ UserProfile model extends the Django `User` model.
    
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_phone = models.CharField(max_length=20, null=True, blank=True)
    default_street_address1 = models.CharField(max_length=80, null=True, blank=True)
    default_street_address2 = models.CharField(max_length=80, null=True, blank=True)
    default_town = models.CharField(max_length=50, null=True, blank=True)
    default_county = models.CharField(max_length=40, null=True, blank=True)
    default_postcode = models.CharField(max_length=9, null=True, blank=True)
    default_country = models.CharField(max_length = 20, default="GB")
    temporary_basket = models.CharField(max_length=600, blank = True)

    def __str__(self):
        return self.user.first_name
    
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """ create or update user profile """
    if created:
        UserProfile.objects.create(user=instance)
    #Exisiting users: just save the profile
    instance.userprofile.save()

