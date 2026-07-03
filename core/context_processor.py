from django.db.models import Q
from .models import Postage, Announcements, SaleSettings, ShopContactInfo

def postage_settings(request):
    """
    Function returns the most recently updated instance of the :model:`Postage`

    **Context**
    ``small_first_class``
    cost, weight, number of balls (size) for this postal class

    ``small_second_class``
    cost, weight, number of balls (size) for this postal class

    ``large_first_class``
    cost, weight, number of balls (size) for this postal class

    ``large_second_class``
    cost, weight, number of balls (size) for this postal class

    """
    query_sm_first = Q(parcel_size=0) & Q(postage_class=1)
    small_first_class = Postage.objects.filter(query_sm_first)[0]
    
    query_sm_second = Q(parcel_size=0) & Q(postage_class=0)
    small_second_class = Postage.objects.filter(query_sm_second)[0]

    query_lg_first = Q(parcel_size=1) & Q(postage_class=1)
    large_first_class = Postage.objects.filter(query_lg_first)[0]

    query_lg_second = Q(parcel_size=1) & Q(postage_class=0)
    large_second_class = Postage.objects.filter(query_lg_second)[0]

    return{
        'small_first_class':small_first_class,
        'small_second_class':small_second_class,
        'large_first_class':large_first_class,
        'large_second_class':large_second_class,
    }

def announcement_banner(request):
    """ Function returns the most recent instance of :model:`Announcements`
    
    **Context**
    ``announcement``
    Criteria and discount rates for bulk buy.

    """
    data = Announcements.objects.all()[0]

    return{
        'announcement':data,
    }

def sale_rate(request):
    """ 
    Function returns the most recently updated instance of the :model:`SaleSettings`
    which is active.

    **Context**
    ``rate`` 
    Discount percentage to be applied to products which are on offer.

    """
    rate = SaleSettings.objects.filter(active=True)[0]

    return{
        'rate':rate,
    }

def shop_address(request):
    """
    Function returns the most recently updated instance of the :model:`ShopContactInfo`

    **Context**
    `contact`
    Contact information for the business
    
    """
    contact = ShopContactInfo.objects.all()[0]
    phone_num = f'0{contact.shop_phone}'

    return{
        'shop_contact': contact,
        'phone_num':phone_num
    }