from django import forms
import django_filters
from .models import Product, Brand


class YarnFilter(django_filters.FilterSet):
    
    brand = django_filters.MultipleChoiceFilter(
        queryset = Brand.objects.all(), 
        field_name= "brand__name",
        to_field_name ="name",
        widget= forms.CheckboxSelectMultiple(),
        label="Brand")

    class Meta:
        model = Product
        fields = ['brand']