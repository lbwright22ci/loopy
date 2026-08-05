from django import forms
from .models import Order

class ContactAndBillingForm(forms.ModelForm):
    """ Creates a :form: from the :model:`checkout.Order

    Fields collected by this form are 'first_name', 'second_name', 'email', 'phone', 
    'billing_street_address1', 'billing_street_address2', 'billing_town', 'billing_county', 'billing_postcode',
    'billing_country' and 'billing_shipping_same'
    """
    
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

    """ 
    Creates a :form: from the :model:`checkout.Order
        
    Fields collected by this form are 
    'shipping_street_address1', 'shipping_street_address2', 'shipping_town', 'shipping_county', 'shipping_postcode',
    'shipping_country', 'is_gift' and 'gift_message'
    """
    
    is_gift = forms.BooleanField(
            required=False, label="Order is a gift")
    
    class Meta:
        model= Order
        fields= ( 'shipping_street_address1', 'shipping_street_address2',
                'shipping_town', 'shipping_county', 'shipping_postcode', 'is_gift', 'gift_message',)
        
    def __init__(self, *args,**kwargs):
        super().__init__(*args, **kwargs)
        self.fields['shipping_street_address1'].widget.attrs['autofocus'] = True
        self.fields['gift_message'].widget = forms.Textarea(attrs={'rows':2})


class SaveDetailsForm(forms.Form):
    """
    Field collected by this :form: is 'save_details'
    """
    save_details = forms.BooleanField(required= False, label="Save billing Address details to my account")

    def __init__(self, *args,**kwargs):
        super().__init__(*args, **kwargs)

