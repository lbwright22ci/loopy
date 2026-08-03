from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from checkout.models import ReviewYarns

class DetailsForm(forms.ModelForm):
    """ Creates :form: from the :model:`core.UserProfile`
    Fields collected by the form are 'user__first_name', 'user__second_name' 'user__email', 'default_email'
    """
    Phone = forms.IntegerField(required=False)

    class Meta:
        model = User
        fields =['first_name', 'last_name',]
    
    def __init__(self, *args, **kwargs):
        super(DetailsForm, self).__init__(*args, **kwargs)
        """
        Adjust the widget attributes attached to first name
        """
        self.fields['first_name'].widget.attrs['autofocus'] = True

class AddressForm(forms.ModelForm):
    """ Creates :form: from the :model:`core.UserProfile`
    Fields collected by the form are 'user__first_name', 'user__second_name' 'user__email', 'default_email'
    """
    class Meta:
        model = UserProfile
        fields =['default_street_address1', 'default_street_address2', 'default_town', 
                 'default_county', 'default_postcode', 'default_country', ]
    
    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        """
        Adjust the widget attributes attached to default street address 1
        """
        self.fields['default_street_address1'].widget.attrs['autofocus'] = True


class ReviewYarnForm(forms.ModelForm):

    class Meta:
        model=ReviewYarns
        fields=['rating', 'comment',]

    def __init__(self, *args, **kwargs):
        super(ReviewYarnForm, self).__init__(*args, **kwargs)
        """
        Adjust the widget attributes attached to 'comment'
        """
        self.fields['comment'].widget = forms.Textarea(attrs={'rows':3})
