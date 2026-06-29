from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class UserProfile(models.Model):
    """ UserProfile model is related to :model:`User`
    
    The fields of this model are `default phone`, `default street address1`,
    `default street address 2`, `default town`, `default county`, 
    `default postcode`, `default country`, `temporary basket`

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
    """ When :model:`User` is updated or created, :model:`UserProfile`
     is also either created or updated """

    if created:
        UserProfile.objects.create(user=instance)
    
    instance.userprofile.save()

class Postage(models.Model):
    """ Used to create and store postage rates for different sized parcels.

    Fields of this model are `postage cost`, `postage class`, `parcel size`,
    `max weight`, `max no balls` and `updated on`
    """
    PCLASS = ((0, "2nd class"), (1, "1st class"))
    PSIZE = ((0, "small"), (1, "medium"))

    postage_cost = models.DecimalField(max_digits= 5, decimal_places = 2, blank= False)
    postage_class = models.IntegerField(choices = PCLASS, default = 0)
    parcel_size = models.IntegerField(choices = PSIZE, default = 0)
    max_weight = models.IntegerField(default =2, verbose_name = "max weight in kg")
    max_no_balls = models.IntegerField(verbose_name = "max number of balls for parcel size", default = 50)
    updated_on = models.DateTimeField(auto_now = True)

    class Meta:
        ordering = ['-updated_on']