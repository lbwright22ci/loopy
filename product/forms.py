from django import forms
from .models import Colour_cat

class ColourVarForm(forms.ModelForm):
    """ """
    class Meta:
        model= Colour_cat
        fields=['colour_name']
