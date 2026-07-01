from django.shortcuts import render, get_object_or_404
from django.contrib import messages

from .models import Contact
from .forms import ContactForm
from core.models import HomePageSlides

# Create your views here.

def contact_page(request):
    """ Renders contact page containing a single instance of :form:`Contact Form`
    to capture inform"""

    top_image = HomePageSlides.objects.all()[1:1]
    bottom_image = HomePageSlides.objects.all()[2:2]

    form = ContactForm()


    context ={ 
        'form': form,
        'top_image':top_image,
        'bottom_image':bottom_image,
              }
    template = 'get_in_touch/contact-page.html'

    return render(request, template, context)
