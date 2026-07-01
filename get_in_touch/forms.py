from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields =('name', 'email', 'subject',
             'message',)
    
    def __init__(self, *args, **kwargs):
        """
        Sets autofocus on first field
        """
        self.fields['name'].widget.attrs['autofocus'] = True
