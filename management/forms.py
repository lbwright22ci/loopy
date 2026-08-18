from django import forms
from core.models import ShopContactInfo


class ShopContactInfoForm(forms.ModelForm):
    """Creates :form: from the :model:`ShopContactInfo`

    Fields are 'shop_email', 'shop_phone', 'shop_street_address1', 'shop_street_address2',
    'shop_town', 'shop_county', 'shop_country', 'shop_postcode'
    """
    class Meta:
        model = ShopContactInfo
        fields = ['shop_email', 'shop_phone', 'shop_street_address1', 'shop_street_address2',
                  'shop_town', 'shop_county', 'shop_country', 'shop_postcode',]

    def __init__(self, *args, **kwargs):
        super(ShopContactInfoForm, self).__init__(*args, **kwargs)
        self.fields['shop_email'].widget.attrs['autofocus'] = True
