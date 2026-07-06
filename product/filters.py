from django import forms
import django_filters
from .models import Product, Brand, Thickness, Colour_var


class YarnFilter(django_filters.FilterSet):
    
    brand_id = django_filters.ModelMultipleChoiceFilter(
        queryset = Brand.objects.all(), 
        to_field_name='id',
        widget= forms.CheckboxSelectMultiple(),
        label = 'Brand',
        label_suffix ="",
        )

    thickness_id = django_filters.ModelMultipleChoiceFilter(
        queryset= Thickness.objects.all(),
        to_field_name='id',
        widget=forms.CheckboxSelectMultiple(),
        label="Thickness",
        label_suffix="",
    )

    # colour_var = django_filters.ModelMultipleChoiceFilter(
    #     queryset=Colour_var.objects.all(),
    #     to_field_name='id',
    #     widget=forms.CheckboxSelectMultiple(),
    #     label="Colour",
    # )

    class Meta:
        model = Product
        fields = [ 
                  'fibre'
                  ]