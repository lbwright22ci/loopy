from django.db import models
from django.db.models import Q
from django.utils.text import slugify

# Create your models here.
class Brand(models.Model):
    """ Stores instances of yarn brands 
    
    Fields included in this model are 'name', 'manufacturer_patterns'
    """
    name = models.CharField(max_length=20, unique=True)
    manufacturer_patterns = models.URLField(max_length=1024, blank = True)

    def __str__(self):
        return f'{self.name}'
    
class Thickness(models.Model):
    """ Stores instances of yarn thickness
    
    Fields include 'name' and 'alt_names'
    """
    name= models.CharField(max_length=20, unique=True)
    alt_names = models.CharField(max_length=100, blank = True, verbose_name ="US terminology")

    class Meta:
        verbose_name_plural = 'Thicknesses'

    def __str__(self):
        return f'{self.name}'
    
class Shade_Type(models.Model):
    """ Stores instances of shade type so that specific colours can be grouped into generic terms
    
    Fields include 'name'
    """
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f'{self.name}'
    
class Colour_cat(models.Model):
    """ Stores instances of specific shades of yarn. Each instance is related to :model:`shade_type`
    
    Fields include 'colour_name', 'image' and 'shade_type_id' """
    colour_name = models.CharField(max_length=40, unique=True)
    image = models.ImageField(blank=True, null=True)
    shade_type_id = models.ForeignKey('Shade_Type', null=True, blank=True, on_delete=models.SET_NULL, related_name = "shade_type")

    def __str__(self):
        return f'{self.colour_name}'
    
class Product(models.Model):
    """ Stores instances of yarn products. Foreign keys are :model:`Brand` and :model:`Thickness` 
    
    Fields include 'brand_id', 'thinkness_id', 'name', 'summary', 'price', 'fibre', 
    'skein_weight', 'skein_length', 'needle_size' , 'knitting_tension', 'machine_wash'
    'wash_temp', 'tumble_dry', 'wool_cycle', 'slug', 'sku', 'visible', 'on_promotion'
    'image
    """
    brand_id = models.ForeignKey('Brand', null=True, blank=True, on_delete=models.CASCADE, related_name = "brand")
    thickness_id = models.ForeignKey('Thickness', null=True, blank=True, on_delete=models.SET_NULL, related_name ="thickness")
    name = models.CharField(max_length=200, null=False)
    summary = models.CharField(max_length=500, null=True, blank= True)
    price = models.DecimalField(max_digits=6, decimal_places=2, blank = False, verbose_name="Price in £")
    fibre = models.CharField(max_length=500, null=True, blank= True)
    natural_fibres = models.BooleanField(default = False)
    skein_weight = models.IntegerField(blank = False, null=False, verbose_name='Weight of single ball in g')
    skein_length = models.IntegerField(blank = True, null=True, verbose_name="Length of yarn in a single ball in m")
    needle_size = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, verbose_name="recommended knitting needle size in mm")
    knitting_tension = models.CharField(max_length=300, blank= True, null=True, verbose_name="st and row count to produce 10 x 10 cm square")
    machine_wash = models.BooleanField(default=False)
    wash_temp = models.IntegerField(blank= True, null=True, verbose_name="Washing Temperature in deg C")
    tumble_dry = models.BooleanField(default=False)
    dry_flat = models.BooleanField(default=False)
    wool_cycle = models.BooleanField(default=False)
    slug= models.SlugField(editable = False, max_length=500)
    sku = models.CharField(max_length=5, unique=True, blank = False)
    visible = models.BooleanField(default = False)
    on_promotion = models.BooleanField(default = False)
    image = models.ImageField(blank = True, null=True)

    class Meta:
        ordering=['name'] 

    def __str__(self):
        return f'{self.brand_id.name} {self.name}, {self.skein_weight}g'

    def save(self):
        """ Generates slug if not present"""
        if not self.slug:
            ss = f'{self.brand_id.name}-{self.name}-{self.skein_weight}'
            self.slug = slugify(ss)

        if not self.natural_fibres:
            if self.fibre.__contains__('crylic')|(self.fibre.__contains__('iscose'))|(self.fibre.__contains__('oly'))|(self.fibre.__contains__('ylon'))| self.fibre.__contains__('henille'):
                self.natural_fibres = False
            else:
                self.natural_fibres = True

        super(Product, self).save()

class Colour_var(models.Model):
    """" This model stores instances of each specific product- the yarn type (:model:`Product`) and the 
    specific colour option (:model:`Colour`)
    
    Fields include 'product_id', 'colour_cat_id', 'shade_code', 'dye_lot', 'low_stock'
    """
    product_id = models.ForeignKey('Product', null=False, blank =False, on_delete=models.CASCADE, related_name='product')
    colour_cat_id = models.ForeignKey('Colour_cat', null=True, blank = True, on_delete=models.SET_NULL, related_name='colour')
    shade_code = models.IntegerField(null=False, blank = False)
    dye_lot = models.IntegerField(blank= False, null=False)
    low_stock = models.BooleanField(default= False)

    def __str__(self):
        return f'{self.product_id.name} colour option {self.colour_cat_id.colour_name}' 

