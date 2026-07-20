from django.shortcuts import render

# Create your views here.

def checkout(request):


    context={}
    template= 'checkout/checkout.html'

    return render(request, template, context)