from django import forms
from .models import Order

class ContactAndBillingForm(forms.ModelForm):
    
    billing_shipping_same = forms.BooleanField(
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
    def __init__(self, *args,**kwargs):
        super().__init__(*args, **kwargs)
        self.fields['shipping_street_address1'].widget.attrs['autofocus'] = True
        

class ExtraDetailsForm(forms.ModelForm):

    is_gift = forms.BooleanField(
        required=False, label="Order is a gift")
    
    class Meta:
        model= Order
        fields = ('is_gift', 'gift_message',)

    def __init__(self, *args,**kwargs):
        super().__init__(*args, **kwargs)
        self.fields['is_gift'].widget.attrs['autofocus'] = True
        self.fields['gift_message'].widget = forms.Textarea(attrs={'rows':2})