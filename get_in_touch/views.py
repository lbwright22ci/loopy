from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .models import Contact
from .forms import ContactForm
from core.models import ShopContactInfo
from core.models import HomePageSlides

# Create your views here.

def contact_page(request):
    """ Renders contact page containing a single instance of :form:`Contact Form`
    to capture inform"""

    top_image = HomePageSlides.objects.all()[1]
    bottom_image = HomePageSlides.objects.all()[2]
    phone = ShopContactInfo.objects.all()[0].shop_phone

    if request.method == "POST":
        form = ContactForm(data=request.POST)
        if form.is_valid():
            in_touch= form.save(commit=False)
            messages.add_message(
                request, messages.SUCCESS,
                'Thank you for contacting Loopy Yarns UK.  We will'
                ' be in touch as soon as possible.  Please check your'
                ' "spam" or "junk" folder if you have not heard from us'
                ' within 2 working days.'
            )
            send_mail(
                "Thank you for contacting Loopy Yarns!",
                render_to_string(
                    'get_in_touch/email/contact_received.txt',
                    { 'in_touch': in_touch,
                      'phone': phone},
                ),
                settings.DEFAULT_FROM_EMAIL,
                [ in_touch.email ],
                fail_silently=False,
            )
            in_touch.save()

    form = ContactForm()

    context ={ 
        'form': form,
        'top_image':top_image,
        'bottom_image':bottom_image,
              }
    template = 'get_in_touch/contact-page.html'

    return render(request, template, context)
