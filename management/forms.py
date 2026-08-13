from django import forms
from core.models import ShopContactInfo

class ShopContactInfoForm(forms.ModelForm):
    """ """
    class Meta:
        model = ShopContactInfo
        fields = ['shop_email', 'shop_phone', 'shop_street_address1', 'shop_street_address2',
                  'shop_town', 'shop_county', 'shop_country', 'shop_postcode',]

    def __init__(self, *args, **kwargs):
        super(ShopContactInfoForm, self).__init__(*args, **kwargs)
        self.fields['shop_email'].widget.attrs['autofocus'] = True


# class BulkAnnouncementsForm(forms.ModelForm):
#     """ """
#     class Meta:
#         model = Announcements
#         fields = ['lower_ball_num', 'lower_discount', 'upper_ball_num', 'upper_discount']
#         labels ={
#             'lower_ball_num': 'Min. no. balls for lower discount',
#             'upper_ball_num': 'Min. no. balls for upper discount',
#             'lower_discount': 'Lower discount',
#             'upper_discount': 'Upper discount',
#         }

#     def __init__(self, *args, **kwargs):
#         super(BulkAnnouncementsForm, self).__init__(*args, **kwargs)
#         self.fields['lower_ball_num'].widget.attrs['autofocus'] = True

# class ShippingAnnouncementsForm(forms.ModelForm):
#     """ """
#     class Meta:
#         model = Announcements
#         fields = ['upper_ball_num',]
#         labels = {
#             'upper_ball_num': 'Min. no. of balls for free shipping'
#         }

#     def __init__(self, *args, **kwargs):
#         super(ShippingAnnouncementsForm, self).__init__(*args, **kwargs)
#         self.fields['upper_ball_num'].widget.attrs['autofocus'] = True