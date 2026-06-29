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
        verbose_name_plural = "Postage"

class Announcements(models.Model):
    """ Used to control text in the annoucement banner at the top of all pages as
    well as conditions for bulk buy discounts
    
    fields in this model are: `bulk buy`, `lower ball num`, `lower discount`, 
    `upper ball num`, `upper discount`, `active`, `updated on`

    Announcement displayed is the most recently updated instance of this model.
    If bulk buy = false, free shipping is offered on orders containing more than
    `upper ball num` balls of yarn.
    If `bulk buy` = true, lower discount% for orders over lower ball num balls of yarn
    and upper discount% for orders over upper ball num balls of yarn
    """

    bulk_buy = models.BooleanField(default= True)
    lower_ball_num = models.IntegerField(blank = True , verbose_name = "number of balls in small bulk buy")
    lower_discount = models.IntegerField(verbose_name= "percentage discount for small bulk buy", blank = True) 
    upper_ball_num = models.IntegerField(blank = True, verbose_name = "number of balls for large bulk buy")
    upper_discount = models.IntegerField(verbose_name= "percentage discount for large bulk buy", blank = True) 
    active = models.BooleanField(default = False)
    updated_on = models.DateTimeField(auto_now = True)

    class Meta:
        ordering = ['-updated_on']
        verbose_name_plural = "Announcements"

class SaleSettings(models.Model):
    """ 
    Used to set the discount rate for sale items.

    Fields in this model are `sales percent`, `active` and `updated on`
    """
    sale_percent= models.IntegerField(default = 0, verbose_name = "percentage discount for sale items")
    active= models.BooleanField(default = False)
    updated_on= models.DateTimeField(auto_now = True)

    class Meta:
        ordering = ['-updated_on']
        verbose_name_plural = "Sale Settings"

class ShopContactInfo(models.Model):
    """"
    Stores Shop contact information

    Fields in this model are `shop email`, `shop phone`, `shop street address1`, 
    `shop street address 2`, `shop town`, `shop county`, `shop country`, 
    `shop postcode`, `updated on`
    """
    shop_email = models.EmailField(blank = True) 
    shop_phone = models.IntegerField(blank = True ) 
    shop_street_address1 = models.CharField(max_length = 80, blank = True )
    shop_street_address2 = models.CharField(max_length = 80, blank = True  )
    shop_town = models.CharField(max_length = 50, blank = True )
    shop_county = models.CharField(max_length = 40, blank = True )
    shop_country = models.CharField(default = "GB"  )
    shop_postcode = models.CharField(max_length= 9, blank = True )
    updated_on = models.DateTimeField(auto_now = True )

    class Meta:
        ordering = ['-updated_on']
        verbose_name_plural = "Shop Contact Information"

class HomePageSlides(models.Model):
    """ Stores images and text displayed on home page carousel

    Fields available are `image`, `title`, `subtitle` and `updated on`
    """
    image = models.ImageField(blank = True, null=True)
    imageURL = models.URLField(max_length=1024, blank=True, null = True)
    title = models.CharField(max_length=400, blank = True)
    subtitle = models.CharField(max_length=400, blank=True)
    updated_on = models.DateTimeField(auto_now= True)

    class Meta:
        ordering =['-updated_on']