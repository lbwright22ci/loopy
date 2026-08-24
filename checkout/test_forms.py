from django.test import TestCase
from .forms import ShippingAddressForm, ContactAndBillingForm

# Create your tests here.


class TestContactAndBillingForm(TestCase):

    def test_form_is_valid(self):
        """ Test that form is valid when all fields are
          completed """
        form = ContactAndBillingForm({
            'first_name': 'name1',
            'second_name': 'name2',
            'phone': 9999,
            'email':'test@test.com',
            'billing_street_address1' : 'street',
            'billing_street_address2' : 'street 2',
            'billing_town' : 'town',
            'billing_county' : 'county',
            'billing_country' : 'country',
            'billing_postcode' : 'postcode',
            'billing_shipping_same' : True
        })
        self.assertTrue(form.is_valid(), msg='Form is not valid')

    def test_form_is_not_valid_if_first_name_missing(self):
        """ Test that form is not valid when first name is not
          completed """
        form = ContactAndBillingForm({
            'first_name': '',
            'second_name': 'name2',
            'phone': 7989,
            'email':'test@test.com',
            'billing_street_address1' : 'street',
            'billing_street_address2' : 'street 2',
            'billing_town' : 'town',
            'billing_county' : 'county',
            'billing_country' : 'country',
            'billing_postcode' : 'postcode',
            'billing_shipping_same' : True
        })
        self.assertFalse(form.is_valid(), msg='Form is valid first name missing')

    def test_form_is_not_valid_if_second_name_missing(self):
        """ Test that form is not valid when second name is not
          completed """
        form = ContactAndBillingForm({
            'first_name': 'name1',
            'second_name': '',
            'phone': 7989789,
            'email':'test@test.com',
            'billing_street_address1' : 'street',
            'billing_street_address2' : 'street 2',
            'billing_town' : 'town',
            'billing_county' : 'county',
            'billing_country' : 'country',
            'billing_postcode' : 'postcode',
            'billing_shipping_same' : True
        })
        self.assertFalse(form.is_valid(), msg='Form is valid with missing second name')

    def test_form_is_not_valid_if_phone_missing(self):
        """ Test that form is not valid when phone is not
          completed """
        form = ContactAndBillingForm({
            'first_name': 'name1',
            'second_name': 'name2',
            'phone': '',
            'email':'test@test.com',
            'billing_street_address1' : 'street',
            'billing_street_address2' : 'street 2',
            'billing_town' : 'town',
            'billing_county' : 'county',
            'billing_country' : 'country',
            'billing_postcode' : 'postcode',
            'billing_shipping_same' : True
        })
        self.assertFalse(form.is_valid(), msg='Form is valid without phone')

    def test_form_is_not_valid_if_email_missing(self):
        """ Test that form is not valid when email is not
          completed """
        form = ContactAndBillingForm({
            'first_name': 'name1',
            'second_name': 'name2',
            'phone': 89089,
            'email':'',
            'billing_street_address1' : 'street',
            'billing_street_address2' : 'street 2',
            'billing_town' : 'town',
            'billing_county' : 'county',
            'billing_country' : 'country',
            'billing_postcode' : 'postcode',
            'billing_shipping_same' : True
        })
        self.assertFalse(form.is_valid(), msg='Form is valid without email')

    def test_form_is_not_valid_if_billing_street_address1_missing(self):
        """ Test that form is not valid when billing street address 1 is not
          completed """
        form = ContactAndBillingForm({
            'first_name': 'name1',
            'second_name': 'name2',
            'phone': 80980890,
            'email':'test@test.com',
            'billing_street_address1' : '',
            'billing_street_address2' : 'street 2',
            'billing_town' : 'town',
            'billing_county' : 'county',
            'billing_country' : 'country',
            'billing_postcode' : 'postcode',
            'billing_shipping_same' : True
        })
        self.assertFalse(form.is_valid(), msg='Form is valid if street address 1 missing')

    def test_form_is_valid_if_billing_street_address2_missing(self):
        """ Test that form is not valid when billing street address 2 is not
          completed """
        form = ContactAndBillingForm({
            'first_name': 'name1',
            'second_name': 'name2',
            'phone': 79878,
            'email':'test@test.com',
            'billing_street_address1' : 'street',
            'billing_street_address2' : '',
            'billing_town' : 'town',
            'billing_county' : 'county',
            'billing_country' : 'country',
            'billing_postcode' : 'postcode',
            'billing_shipping_same' : True
        })
        self.assertTrue(form.is_valid(), msg='Form is not valid with street address 2 missing')

    def test_form_is_not_valid_if_billing_town_missing(self):
        """ Test that form is not valid when billing town is not
          completed """
        form = ContactAndBillingForm({
            'first_name': 'name1',
            'second_name': 'name2',
            'phone': 79880890,
            'email':'test@test.com',
            'billing_street_address1' : 'street',
            'billing_street_address2' : 'street 2',
            'billing_town' : '',
            'billing_county' : 'county',
            'billing_country' : 'country',
            'billing_postcode' : 'postcode',
            'billing_shipping_same' : True
        })
        self.assertFalse(form.is_valid(), msg='Form is valid with billing town missing')

    def test_form_is_not_valid_if_billing_county_missing(self):
        """ Test that form is not valid when billing county is not
          completed """
        form = ContactAndBillingForm({
            'first_name': 'name1',
            'second_name': 'name2',
            'phone': 79887989,
            'email':'test@test.com',
            'billing_street_address1' : 'street',
            'billing_street_address2' : 'street 2',
            'billing_town' : 'town',
            'billing_county' : '',
            'billing_country' : 'country',
            'billing_postcode' : 'postcode',
            'billing_shipping_same' : True
        })
        self.assertFalse(form.is_valid(), msg='Form is valid with county missing')

    def test_form_is_not_valid_if_billing_country_missing(self):
        """ Test that form is not valid when billing country is not
          completed """
        form = ContactAndBillingForm({
            'first_name': 'name1',
            'second_name': 'name2',
            'phone': 77989,
            'email':'test@test.com',
            'billing_street_address1' : 'street',
            'billing_street_address2' : 'street 2',
            'billing_town' : 'town',
            'billing_county' : 'county',
            'billing_country' : '',
            'billing_postcode' : 'postcode',
            'billing_shipping_same' : True
        })
        self.assertFalse(form.is_valid(), msg='Form is valid country missing')

    def test_form_is_not_valid_if_billing_postcode_missing(self):
        """ Test that form is not valid when billing postcode is not
          completed """
        form = ContactAndBillingForm({
            'first_name': 'name1',
            'second_name': 'name2',
            'phone': 79870,
            'email':'test@test.com',
            'billing_street_address1' : 'street',
            'billing_street_address2' : 'street 2',
            'billing_town' : 'town',
            'billing_county' : 'county',
            'billing_country' : 'country',
            'billing_postcode' : '',
            'billing_shipping_same' : True
        })
        self.assertFalse(form.is_valid(), msg='Form is valid without billing postcode')


class TestShippingForm(TestCase):

    def test_form_is_valid(self):
        """ Test that form is valid when all fields are
          completed """
        form = ShippingAddressForm({
            'shipping_street_address1' : 'street',
            'shipping_street_address2' : 'street 2',
            'shipping_town' : 'town',
            'shipping_county' : 'county',
            'shipping_country' : 'country',
            'shipping_postcode' : 'postcode',
            'is_gift':True,
            'gift_message':'gift message'
        })
        self.assertTrue(form.is_valid(), msg='Form is not valid')

    def test_form_is_not_valid_with_street_address1_missing(self):
        """ Test that form is valid when shipping address 1 not completed
          completed """
        form = ShippingAddressForm({
            'shipping_street_address1' : '',
            'shipping_street_address2' : 'street 2',
            'shipping_town' : 'town',
            'shipping_county' : 'county',
            'shipping_country' : 'country',
            'shipping_postcode' : 'postcode',
            'is_gift':True,
            'gift_message':'gift message'
        })
        self.assertFalse(form.is_valid(), msg='Form is valid without shipping address 1')

    def test_form_is_valid_with_street_address2_missing(self):
        """ Test that form is valid when shipping address 2 not completed
          completed """
        form = ShippingAddressForm({
            'shipping_street_address1' : 'street',
            'shipping_street_address2' : '',
            'shipping_town' : 'town',
            'shipping_county' : 'county',
            'shipping_country' : 'country',
            'shipping_postcode' : 'postcode',
            'is_gift':True,
            'gift_message':'gift message'
        })
        self.assertTrue(form.is_valid(), msg='Form is not valid without shipping address 2')

    def test_form_is_not_valid_with_town_missing(self):
        """ Test that form is valid when shipping town not completed
          completed """
        form = ShippingAddressForm({
            'shipping_street_address1' : 'street',
            'shipping_street_address2' : 'street 2',
            'shipping_town' : '',
            'shipping_county' : 'county',
            'shipping_country' : 'country',
            'shipping_postcode' : 'postcode',
            'is_gift':True,
            'gift_message':'gift message'
        })
        self.assertFalse(form.is_valid(), msg='Form is valid without shipping town')

    def test_form_is_not_valid_with_county_missing(self):
        """ Test that form is valid when shipping county not completed
          completed """
        form = ShippingAddressForm({
            'shipping_street_address1' : 'street',
            'shipping_street_address2' : 'street 2',
            'shipping_town' : 'town',
            'shipping_county' : '',
            'shipping_country' : 'country',
            'shipping_postcode' : 'postcode',
            'is_gift':True,
            'gift_message':'gift message'
        })
        self.assertFalse(form.is_valid(), msg='Form is valid without shipping county')

    def test_form_is_not_valid_with_country_missing(self):
        """ Test that form is valid when shipping country not completed
          completed """
        form = ShippingAddressForm({
            'shipping_street_address1' : 'street',
            'shipping_street_address2' : 'street 2',
            'shipping_town' : 'town',
            'shipping_county' : 'county',
            'shipping_country' : '',
            'shipping_postcode' : 'postcode',
            'is_gift':True,
            'gift_message':'gift message'
        })
        self.assertTrue(form.is_valid(), msg='Form is not valid without shipping country')

    def test_form_is_not_valid_with_postcode_missing(self):
        """ Test that form is valid when shipping postcode not completed
          completed """
        form = ShippingAddressForm({
            'shipping_street_address1' : 'street',
            'shipping_street_address2' : 'street 2',
            'shipping_town' : 'town',
            'shipping_county' : 'county',
            'shipping_country' : 'country',
            'shipping_postcode' : '',
            'is_gift':True,
            'gift_message':'gift message'
        })
        self.assertFalse(form.is_valid(), msg='Form is valid without postcode')

    def test_form_is_valid_with_gift_message_missing(self):
        """ Test that form is valid when gift message not completed
          completed """
        form = ShippingAddressForm({
            'shipping_street_address1' : 'street',
            'shipping_street_address2' : 'street 2',
            'shipping_town' : 'town',
            'shipping_county' : 'county',
            'shipping_country' : 'country',
            'shipping_postcode' : 'postcode',
            'is_gift':True,
            'gift_message':''
        })
        self.assertTrue(form.is_valid(), msg='Form is not valid without gift message')

