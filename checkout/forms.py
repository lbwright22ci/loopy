from django import forms
from .models import Order

class ContactAndBillingForm(forms.ModelForm):
    
    CHOICES =[(True, 'yes'), (False, 'no')]
    billing_shipping_same = forms.BooleanField(widget=forms.RadioSelect(choices=CHOICES),
        required=False, label="Use Billing address for shipping")

    class Meta:
        model= Order
        fields= ('first_name', 'second_name', 'email', 'phone', 
                'billing_street_address1', 'billing_street_address2',
                'billing_town', 'billing_county', 'billing_postcode',
                'billing_country',)
        
    def __init__(self, *args,**kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['autofocus'] = True

class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model= Order
        fields= ( 'shipping_street_address1', 'shipping_street_address2',
                'shipping_town', 'shipping_county', 'shipping_postcode',
                )
        
class PostageForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('postage_class',)

class ExtraDetailsForm(forms.ModelForm):
    class Meta:
        model= Order
        fields = ('is_gift', 'gift_message',)