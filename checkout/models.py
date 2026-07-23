import uuid
import json
from decimal import Decimal
from django.db import models
from django.db.models import Sum, Q
from core.models import UserProfile, SaleSettings, Announcements, Postage
from product.models import Colour_var, Product

# Create your models here.


class Order(models.Model):
    """ """

    PCLASS = ((0, "2nd class"), (1, "1st class"))
    PSIZE = ((0, "small"), (1, "medium"))

    created_on= models.DateTimeField(auto_now=True)
    order_num = models.CharField(max_length=8, null=False, editable=False)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, blank=True, null=True, related_name="orders")
    first_name= models.CharField(max_length=20, blank = False, null=False)
    second_name= models.CharField(max_length=20, blank = False, null=False)
    email = models.EmailField(blank=False, null=False)
    phone = models.IntegerField(null=True, blank=True)
    billing_street_address1 = models.CharField(max_length=80, null=False, blank=False, verbose_name='Street Address 1', help_text="Orders can only be shipped to UK addresses")
    billing_street_address2 = models.CharField(max_length=80, null=True, blank=True, verbose_name='Street Address 2')
    billing_town = models.CharField(max_length=50, null=False, blank=False, verbose_name="Town or City")
    billing_county = models.CharField(max_length=40, null=False, blank=False, verbose_name='County')
    billing_postcode = models.CharField(max_length=9, null=False, blank=False, verbose_name='Postcode')
    billing_country = models.CharField(max_length = 20, default="GB", null=False, verbose_name='Country')
    shipping_street_address1 = models.CharField(max_length=80, null=False, blank=False, verbose_name='Street Address 1', help_text="Orders can only be shipped to UK addresses")
    shipping_street_address2 = models.CharField(max_length=80, null=True, blank=True,  verbose_name='Street Address 2')
    shipping_town = models.CharField(max_length=50, null=False, blank=False,  verbose_name='Town or City')
    shipping_county = models.CharField(max_length=40, null=False, blank=False, verbose_name='County')
    shipping_postcode = models.CharField(max_length=9, null=False, blank=False, verbose_name='Postcode')
    shipping_country = models.CharField(max_length = 20, default="GB", editable=False)
    basket_contents = models.TextField(blank=False, null=False, default = "")
    is_gift = models.BooleanField(default=False, verbose_name="Order is a gift")
    gift_message = models.CharField(max_length=500, blank=True, null=True)
    postage_class = models.IntegerField(choices=PCLASS, default=0)
    parcel_size = models.IntegerField(choices=PSIZE,default=0)
    order_subtotal = models.DecimalField(max_digits=5, decimal_places=2, default=0, null=False)
    order_discount = models.DecimalField(max_digits=5, decimal_places=2, default=0, null=False)
    postage_cost = models.DecimalField(max_digits=5, decimal_places=2, default=0, null=False)
    grand_total = models.DecimalField(max_digits=5, decimal_places=2, default=0, null=False)
    is_shipped = models.BooleanField(default = False)
    use_voucher= models.BooleanField(default= False)
    voucher_amount = models.DecimalField(max_digits=5, decimal_places=2, blank = True, default=0)
    amount_payable = models.DecimalField(max_digits=5, decimal_places=2, blank = False, default=0)
    refund_status = models.BooleanField(default = False)
    stripe_pid = models.CharField(max_length=254, null=False, blank=False, default="")

    def __generate_order_num(self):
        """ """
        return str(uuid.uuid4()).replace('-','')[:8]
    

    def save(self):
        """"""
        if self.pk:
            ball_count = self.lineitems.aggregate(Sum('quantity'))['quantity__sum'] or 0
            self.order_subtotal = self.lineitems.aggregate(Sum('linetotal'))['linetotal__sum'] or 0

            bulk_buy = Announcements.objects.filter(active=True)[0]
            
            yarn_weight = self.lineitems.aggregate(Sum('lineweight'))['lineweight__sum'] or 0
            
            if ball_count < 5:
                yarn_weight = yarn_weight + 200
            else:
                yarn_weight = yarn_weight + 400
            
            small_ball_limit = Postage.objects.filter(Q(parcel_size=0) & Q(postage_class=0))[0].max_no_balls
            small_weight_limit = Postage.objects.filter(Q(parcel_size=0) & Q(postage_class=0))[0].max_weight*1000
            

            if ball_count < small_ball_limit and yarn_weight < small_weight_limit:
                self.parcel_size = 0
                self.postage_cost = Postage.objects.filter(Q(parcel_size=self.parcel_size) & Q(postage_class=self.postage_class))[0].postage_cost
            else:
                self.parcel_size = 1
                self.postage_cost = Postage.objects.filter(Q(parcel_size=self.parcel_size) & Q(postage_class=self.postage_class))[0].postage_cost

            if bulk_buy.bulk_buy == True:
                if ball_count > bulk_buy.upper_ball_num:
                    self.order_discount = self.order_subtotal*Decimal((bulk_buy.upper_discount)/100)
                elif ball_count < bulk_buy.lower_ball_num:
                    self.order_discount = 0
                else:
                    self.order_discount = self.order_subtotal*Decimal((bulk_buy.lower_discount)/100)
            else:
                if ball_count > bulk_buy.upper_ball_num:
                    self.order_discount = Postage.objects.filter(Q(parcel_size=self.parcel_size) & Q(postage_class=0))[0].postage_cost
            
            self.grand_total = self.order_subtotal - self.order_discount + self.postage_cost
            if self.use_voucher:
                self.amount_payable = self.grand_total - self.voucher_amount
            else:
                self.amount_payable = self.grand_total
            
            basket = {}
            ylo = YarnOrderLineitem.objects.filter(order__pk = self.pk)
            for i in range(0, ylo.all().count()):
                basket[str(ylo[i].yarn.pk)]= int(ylo[i].quantity)

            self.basket_contents = json.dumps(basket)

        if not self.order_num:
            self.order_num = self.__generate_order_num()
        super(Order, self).save()

    class Meta:
        ordering = ['created_on',]

class YarnOrderLineitem(models.Model):
    """"""
    order= models.ForeignKey(Order, null=False, blank = False, on_delete=models.CASCADE, related_name = "lineitems")
    yarn = models.ForeignKey(Colour_var, null=True, blank = False, on_delete=models.SET_NULL, related_name = 'yarn')
    quantity = models.IntegerField(null=False, blank = False)
    current_price = models.DecimalField(max_digits=5, decimal_places=2, blank = False, editable=False, default=0)
    linetotal = models.DecimalField(max_digits=5, decimal_places=2, blank = False, null=False, editable = False)
    lineweight = models.IntegerField( blank =False, editable=False)


    def save(self):
        """" """
        sale_discount = SaleSettings.objects.filter(active=True)[0].sale_percent
        if self.yarn.product_id.on_promotion:
            self.current_price = Decimal(self.yarn.product_id.price*(100-sale_discount)/100)
        else:
            self.current_price = self.yarn.product_id.price
        self.linetotal = self.current_price * self.quantity
        self.lineweight = self.quantity * self.yarn.product_id.skein_weight
        super(YarnOrderLineitem, self).save()
