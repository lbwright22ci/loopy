from django.test import TestCase
from .forms import DetailsForm, AddressForm

# Create your tests here.


class TestDetailsForm(TestCase):

    def test_form_is_valid(self):
        """ Test that form is valid when all fields are
          completed """
        form = DetailsForm({
            'first_name': 'name1',
            'second_name': 'name2',
            'default_phone': 9999,
        })
        self.assertTrue(form.is_valid(), msg='Form is not valid')

    def test_form_is_valid_if_phone_is_blank(self):
        """ Test that form is declared valid if phone is not
          completed """
        form = DetailsForm({
            'first_name': 'name1',
            'second_name': 'name2',
            'default_phone': '',
        })
        self.assertTrue(
            form.is_valid(), msg='Form is invalid when phone is blank')

    def test_form_is_valid_if_first_name_is_blank(self):
        """ Test that form is declared valid if first name is not completed"""
        form = DetailsForm({
            'first_name': '',
            'second_name': 'name2',
            'default_phone': 9999,
        })
        self.assertTrue(
            form.is_valid(), msg='Form is invalid when first name is blank')

    def test_form_is_invalid_if_second_name_is_blank(self):
        """ Test that form is declared valid if second name is not
        completed"""
        form = DetailsForm({
            'first_name': 'name1',
            'second_name': '',
            'default_phone': 9999,
        })
        self.assertTrue(
            form.is_valid(), msg='Form is invalid when second name is blank')


class TestAddressForm(TestCase):

    def test_form_is_valid(self):
        """ Test that form is valid when all fields are
          completed """
        form = AddressForm({
            'default_street_address1': 'street',
            'default_street_address2': 'street 2',
            'default_town': 'town',
            'default_county': 'county',
            'default_country': 'country',
            'default_postcode': 'postcode'
        })
        self.assertTrue(form.is_valid(), msg='Form is not valid')

    def test_form_is_valid_if_street_address1_blank(self):
        """ Test that form is valid when street address 1 is blank
          completed """
        form = AddressForm({
            'default_street_address1': '',
            'default_street_address2': 'street 2',
            'default_town': 'town',
            'default_county': 'county',
            'default_country': 'country',
            'default_postcode': 'postcode'
        })
        self.assertTrue(
            form.is_valid(),
            msg='Form is not valid when street address 1 is blank')

    def test_form_is_valid_if_street_address2_blank(self):
        """ Test that form is valid when street address 2 is blank
          completed """
        form = AddressForm({
            'default_street_address1': 'street',
            'default_street_address2': '',
            'default_town': 'town',
            'default_county': 'county',
            'default_country': 'country',
            'default_postcode': 'postcode'
        })
        self.assertTrue(
            form.is_valid(),
            msg='Form is not valid when street address 2 is blank')

    def test_form_is_valid_if_town_blank(self):
        """ Test that form is valid when town is blank
          completed """
        form = AddressForm({
            'default_street_address1': 'street1',
            'default_street_address2': 'street 2',
            'default_town': '',
            'default_county': 'county',
            'default_country': 'country',
            'default_postcode': 'postcode'
        })
        self.assertTrue(
            form.is_valid(),
            msg='Form is not valid when town is blank')

    def test_form_is_valid_if_county_blank(self):
        """ Test that form is valid when county is blank
          completed """
        form = AddressForm({
            'default_street_address1': 'street',
            'default_street_address2': 'street 2',
            'default_town': 'town',
            'default_county': '',
            'default_country': 'country',
            'default_postcode': 'postcode'
        })
        self.assertTrue(
            form.is_valid(),
            msg='Form is not valid when county is blank')

    def test_form_is_valid_if_country_blank(self):
        """ Test that form is valid when country is blank
          completed """
        form = AddressForm({
            'default_street_address1': 'street',
            'default_street_address2': 'street 2',
            'default_town': 'town',
            'default_county': 'county',
            'default_country': '',
            'default_postcode': 'postcode'
        })
        self.assertTrue(
            form.is_valid(),
            msg='Form is not valid when country is blank')

    def test_form_is_valid_if_postcode_blank(self):
        """ Test that form is valid when postcode is blank
          completed """
        form = AddressForm({
            'default_street_address1': 'street',
            'default_street_address2': 'street 2',
            'default_town': 'town',
            'default_county': 'county',
            'default_country': 'country',
            'default_postcode': ''
        })
        self.assertTrue(
            form.is_valid(),
            msg='Form is not valid when postcode is blank')
