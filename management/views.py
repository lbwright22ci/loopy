from django.shortcuts import render,  redirect, reverse, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.messages import add_message

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

    context={

    }
    template = 'management/admin-settings.html'

    return render(request, template, context)

@login_required
def management_products(request):
    """ """
    if not request.user.is_superuser:
        messages.add_message(request, messages.ERROR, f"This page is only accessible for \
                             Loopy Yarns staff.")
        return redirect(reverse('home'))

    context={

    }
    template = 'management/admin-products.html'

    return render(request, template, context)

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
