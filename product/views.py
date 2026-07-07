from django.shortcuts import render
from django.views import generic
from django.db.models import Q

from django_filters.views import FilterView

from .models import Product, Colour_cat, Colour_var, Brand, Thickness, Shade_Type
from .filters import YarnFilter


# Create your views here.

class AllProductsListView(generic.ListView):
    """" """
    queryset = Product.objects.all()
    paginate_by = 12
    template_name = 'product/all-products.html'
    ordering = ['name']
    context_object_name = 'product_list'

    # def update_fibres():
    #     for product in Product.objects.all():
    #         if product.fibre.__contains__('crylic')|(product.fibre.__contains__('iscose'))|(product.fibre.__contains__('oly'))|(product.fibre.__contains__('ylon'))| product.fibre.__contains__('henille'):
    #             product.natural_fibres = False
    #         else:
    #             product.natural_fibres = True
    #         product.save()
    # update_fibres()

    def get_queryset(self):
        queryset =  super().get_queryset()
        self.filterset = YarnFilter(self.request.GET, queryset = queryset)
        return self.filterset.qs
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['form'] = self.filterset.form
        context['filters'] = self.filterset
        return context