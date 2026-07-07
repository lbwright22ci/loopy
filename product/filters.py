from django import forms
from django.db import models

import django_filters

from .models import Product, Brand, Thickness


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

    FIBRE_CHOICES =(
        ('Alpaca', 'Alpaca'),
        ('Acrylic', 'Acrylic'),
        ('Cotton', 'Cotton'),
        ('Chenille', 'Chenille'),
        ('Merino', 'Merino'),
        ('Wool', 'Wool'),
    )

    fibre__icontains = django_filters.MultipleChoiceFilter(
        choices = FIBRE_CHOICES,
        widget=forms.CheckboxSelectMultiple(),
        label = "Fibre",
    )

    COLOUR_CHOICES=(
        ('yellow', 'Yellow'),
        ('red', 'Red'),
    )

    product__colour_cat_id__in = django_filters.MultipleChoiceFilter(
        choices = COLOUR_CHOICES,
        widget=forms.CheckboxSelectMultiple(),
        label="Colour",
    )

    class Meta:
        model = Product
        fields = [ 'on_promotion', 'machine_wash', 'natural_fibres', 'product__colour_cat_id__in', 'brand_id', 'thickness_id', 'fibre__icontains'
                  ]
        filter_overrides ={
            models.BooleanField:{
                'filter_class':django_filters.BooleanFilter,
                'extra': lambda f:{
                    'widget': forms.CheckboxInput,
                },
            },
        }