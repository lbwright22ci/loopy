from django.shortcuts import get_object_or_404


from core.models import SaleSettings, Postage, Announcements
from product.models import Colour_var

def basket_contents(request):
    basket_items=[]
    total=0
    ball_count = 0

    basket = request.session.get('basket', {})

    for item_id, item_data in basket.items():
        col_var = get_object_or_404(Colour_var, pk = item_id)
        if col_var.on_promotion:
