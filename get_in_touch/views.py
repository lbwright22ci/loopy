from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
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
    phone = f'0{ShopContactInfo.objects.all()[0].shop_phone}'

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
            email_subject ="Thank you for contacting Loopy Yarns!"
            html_message = render_to_string('get_in_touch/email/contact_received.html', 
                                            { 'in_touch': in_touch, 'phone': phone},
                                            )
            plain_message = strip_tags(html_message)

            msg= EmailMultiAlternatives(
                email_subject,
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [ in_touch.email ],
                
            )
            msg.attach_alternative(html_message, "text/html")
            msg.send()
            in_touch.save()
            return redirect('allproducts')
    else:
        form = ContactForm()

    context ={ 
        'form': form,
        'top_image':top_image,
        'bottom_image':bottom_image,
              }
    template = 'get_in_touch/contact-page.html'

    return render(request, template, context)
