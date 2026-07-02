from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    """ Creates :form: from the :model:`get_in_touch.Contact`
    Fields collected by the form are 'name', 'email', 'subject' and 'messsage'
    """
    class Meta:
        model = Contact
        fields =['name', 'email', 'subject',
             'message',]
    
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        """
        Adjust the widget attributes attached to name and message fields
        """
        self.fields['name'].widget.attrs['autofocus'] = True
        self.fields['message'].widget = forms.Textarea(attrs={'rows': 4})