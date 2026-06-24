from django.shortcuts import render

# Create your views here.

def home_page(request):
    """
    Renders the home page for the Loopy e-commerce site

    **Template**
    :template: `home.html`

    """
    template= 'core/home.html'
    context = {}

    return render (request, template, context)