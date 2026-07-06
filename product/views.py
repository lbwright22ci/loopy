from django.shortcuts import render
from django.views import generic

from django_filters.views import FilterView

from .models import Product, Colour_cat, Colour_var, Brand, Thickness, Shade_Type
from .filters import YarnFilter


# Create your views here.

class AllProductsListView(FilterView):
    """" """

    model= Product
    paginate_by= 12
    template_name= 'product/all-products.html'
    ordering =['-skein_weight']
    context_object_name = 'product_list'
    filterset_class = YarnFilter

    # def get_queryset(self):
    #     queryset =  super().get_queryset()
    #     filter = YarnFilter(self.request.GET, queryset)
    #     return filter.qs
    
    # def get_context_data(self, **kwargs):
    #     context =  super().get_context_data(**kwargs)
    #     queryset = self.get_queryset()
    #     filter = YarnFilter(self.request.GET, queryset)
    #     context['form'] = self.filter.form
    #     return context