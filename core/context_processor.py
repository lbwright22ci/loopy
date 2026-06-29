from django.db.models import Q
from .models import Postage

def postage_settings(request):
    # return{
    #    'small_first_class':0,
    #    'small_second_class': 0,
    #    'large_first_class':0,
    #    'large_second_class':0,
# }

    query_sm_first = Q(parcel_size=0) & Q(postage_class=1)
    small_first_class = Postage.objects.filter(query_sm_first)[0].postage_cost
    

    query_sm_second = Q(parcel_size=0) & Q(postage_class=0)
    small_second_class = Postage.objects.filter(query_sm_second)[0].postage_cost

    query_lg_first = Q(parcel_size=1) & Q(postage_class=1)
    large_first_class = Postage.objects.filter(query_lg_first)[0].postage_cost

    query_lg_second = Q(parcel_size=1) & Q(postage_class=0)
    large_second_class = Postage.objects.filter(query_lg_second)[0].postage_cost

    return{
        'small_first_class':small_first_class,
        'small_second_class':small_second_class,
        'large_first_class':large_first_class,
        'large_second_class':large_second_class,
 }