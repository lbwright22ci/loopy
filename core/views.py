from django.shortcuts import render
from .models import HomePageSlides

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