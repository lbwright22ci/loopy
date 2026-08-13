from django.shortcuts import render,  redirect, reverse, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import ShopContactInfoForm
from core.models import SaleSettings, ShopContactInfo, Announcements


# Create your views here.

@login_required
def management_home(request):
    """ """
    if not request.user.is_superuser:
        messages.add_message(request, messages.ERROR, f"This page is only accessible for \
                             Loopy Yarns staff.")
        return redirect(reverse('home'))

    context={

    }
    template = 'management/admin-home.html'

    return render(request, template, context)


@login_required
def management_settings(request):
    """ """
    if not request.user.is_superuser:
        messages.add_message(request, messages.ERROR, f"This page is only accessible for \
                             Loopy Yarns staff.")
        return redirect(reverse('home'))

    shop_details = ShopContactInfo.objects.all()[0]
    shop_form = ShopContactInfoForm(instance = shop_details)

    sale_rate = get_object_or_404(SaleSettings, active = True)
    sale_rate = sale_rate.sale_percent

    announcement = Announcements.objects.all()[0]

    context={
        'shop_form':shop_form,
        'sale_rate' : sale_rate,
        'current':announcement,
    }
    template = 'management/admin-settings.html'

    return render(request, template, context)


@login_required
def update_shopsettings(request):
    """ """
    if not request.user.is_superuser:
            messages.add_message(request, messages.ERROR, f"This page is only accessible for \
                                 Loopy Yarns staff.")
            return redirect(reverse('home'))
    
    shop_details = ShopContactInfo.objects.all()[0]

    try:
        if request.POST:
            shop_form = ShopContactInfoForm(data= request.POST)
            if shop_form.is_valid:
                shop_details.shop_email = request.POST.get('shop_email')
                shop_details.shop_phone = request.POST.get('shop_phone')
                shop_details.shop_street_address1 = request.POST.get('shop_street_address1')
                shop_details.shop_street_address2 = request.POST.get('shop_street_address2')
                shop_details.shop_town = request.POST.get('shop_town')
                shop_details.shop_county = request.POST.get('shop_county')
                shop_details.shop_country = request.POST.get('shop_country')
                shop_details.shop_postcode = request.POST.get('shop_postcode')
                shop_details.save()
                messages.add_message(request, messages.SUCCESS, f'Shop address settings updated!')

    except Exception as e:
        messages.add_message(request, messages.ERROR, f'Unable to update shop settings. Error message: {e}')

    return redirect(reverse('management_settings'))

@login_required
def update_salesettings(request):
    """ """
    if not request.user.is_superuser:
            messages.add_message(request, messages.ERROR, f"This page is only accessible for \
                                 Loopy Yarns staff.")
            return redirect(reverse('home'))
    
    sale = SaleSettings.objects.filter(active=True)[0]

    try:
        if request.POST:
            sale.sale_percent = request.POST.get('sale_percent')
            sale.save()
            messages.add_message(request, messages.SUCCESS, f'Items on sale will now have {sale.sale_percent}% discount applied')

    except Exception as e:
        messages.add_message(request, messages.ERROR, f'Unable to update sale settings. Error message: {e}')

    return redirect(reverse('management_settings'))

@login_required
def management_orders(request):
    """ """
    if not request.user.is_superuser:
        messages.add_message(request, messages.ERROR, f"This page is only accessible for \
                             Loopy Yarns staff.")
        return redirect(reverse('home'))

    context={

    }
    template = 'management/admin-orders.html'

    return render(request, template, context)
