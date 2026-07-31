from django.shortcuts import render, reverse, redirect
from django.contrib import messages
from .models import HomePageSlides, UserProfile
from .forms import AddressForm, DetailsForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def home_page(request):
    """
    Renders the home page for the Loopy e-commerce site, displaying 
    the 5 most recently updated instances of :model:`HomePageSlides`

    **Template**
    :template: `home.html`

    **Context**
    ``slides``

    """

    slides = HomePageSlides.objects.all()[0:5]

    template= 'core/home.html'
    context = {'slides':slides,}

    return render (request, template, context)

@login_required
def customer_account(request):
    """ """
    profile = UserProfile.objects.get(user=request.user)
    past_orders = profile.orders.all().order_by('-created_on')

    details_form = DetailsForm(initial={
                'first_name':profile.user.first_name,
                'last_name':profile.user.last_name,
                'Phone': profile.default_phone,
            })
    address_form = AddressForm(initial={
        'default_street_address1': profile.default_street_address1,
        'default_street_address2': profile.default_street_address2,
        'default_county': profile.default_county,
        'default_country': profile.default_country,
        'default_postcode': profile.default_postcode,
        'default_town': profile.default_town,
            })

    context={
        'address_form':address_form,
        'details_form': details_form,
        'past_orders':past_orders,
    }
    template = 'core/account.html'

    return render(request, template, context)

@login_required
def update_details(request):
    """" """
    current_user = UserProfile.objects.get(user__id= request.user.id)
    try:
        if request.POST:
            details_form = DetailsForm(data=request.POST)
            if details_form.is_valid():
                current_user.user.first_name = request.POST.get('first_name')
                current_user.user.last_name = request.POST.get('last_name')
                current_user.default_phone = request.POST.get('Phone')
                current_user.save()

                messages.add_message(request, messages.SUCCESS, f'Your account details have been updated!')
    except Exception as e:
        messages.add_message(request, messages.ERROR, f'Unable to update your account details. Error message: {e}')

    return redirect(reverse('customer_account'))

@login_required
def update_address(request):
    """" """
    current_user = UserProfile.objects.get(user__id= request.user.id)
    try:
        if request.POST:
            address_form = AddressForm(data=request.POST)
            if address_form.is_valid():
                current_user.default_street_address1 = request.POST.get('default_street_address1')
                current_user.default_street_address2 = request.POST.get('default_street_address2')
                current_user.default_town = request.POST.get('default_town')
                current_user.default_county = request.POST.get('default_county')
                current_user.default_country = request.POST.get('default_country')
                current_user.default_postcode = request.POST.get('default_postcode')
                current_user.save()

                messages.add_message(request, messages.SUCCESS, f'Your address details have been updated!')
    except Exception as e:
        messages.add_message(request, messages.ERROR, f'Unable to update your address details. Error message: {e}')

    return redirect(reverse('customer_account'))