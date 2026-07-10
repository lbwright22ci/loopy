from django import forms
from .models import Colour_var

class ColourVarForm(forms.ModelForm):
    """ """
    class Meta:
        model= Colour_var
        fields=['colour_cat_id']
