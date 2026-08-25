from django.test import TestCase
from .forms import ShopContactInfoForm

# Create your tests here.


class TestShopContactInfoForm(TestCase):

    def test_form_is_valid(self):
        """ Test that form is valid when all fields are
          completed """
        form = ShopContactInfoForm({
            'shop_phone': 9999,
            'shop_email': 'test@test.com',
            'shop_street_address1': 'street',
            'shop_street_address2': 'street 2',
            'shop_town': 'town',
            'shop_county': 'county',
            'shop_country': 'country',
            'shop_postcode': 'postcode',
        })
        self.assertTrue(form.is_valid(), msg='Form is not valid')

    def test_form_is_valid_if_phone_is_blank(self):
        """ Test that form is valid when phone is not
          completed """
        form = ShopContactInfoForm({
            'shop_phone': '',
            'shop_email': 'test@test.com',
            'shop_street_address1': 'street',
            'shop_street_address2': 'street 2',
            'shop_town': 'town',
            'shop_county': 'county',
            'shop_country': 'country',
            'shop_postcode': 'postcode',
        })
        self.assertTrue(
            form.is_valid(),
            msg='Form is not valid when phone is blank')

    def test_form_is_valid_if_email_is_blank(self):
        """ Test that form is valid when email is not
          completed """
        form = ShopContactInfoForm({
            'shop_phone': 10890,
            'shop_email': '',
            'shop_street_address1': 'street',
            'shop_street_address2': 'street 2',
            'shop_town': 'town',
            'shop_county': 'county',
            'shop_country': 'country',
            'shop_postcode': 'postcode',
        })
        self.assertTrue(
            form.is_valid(),
            msg='Form is not valid when email is blank')

    def test_form_is_valid_if_street_address1_is_blank(self):
        """ Test that form is valid when street address 1 is not
          completed """
        form = ShopContactInfoForm({
            'shop_phone': 79879,
            'shop_email': 'test@test.com',
            'shop_street_address1': '',
            'shop_street_address2': 'street 2',
            'shop_town': 'town',
            'shop_county': 'county',
            'shop_country': 'country',
            'shop_postcode': 'postcode',
        })
        self.assertTrue(
            form.is_valid(),
            msg='Form is not valid when street address 1 is blank')

    def test_form_is_valid_if_street_address2_is_blank(self):
        """ Test that form is valid when street address 2 is not
          completed """
        form = ShopContactInfoForm({
            'shop_phone': 7989789,
            'shop_email': 'test@test.com',
            'shop_street_address1': 'street',
            'shop_street_address2': '',
            'shop_town': 'town',
            'shop_county': 'county',
            'shop_country': 'country',
            'shop_postcode': 'postcode',
        })
        self.assertTrue(
            form.is_valid(),
            msg='Form is not valid when street address 2 is blank')

    def test_form_is_valid_if_town_is_blank(self):
        """ Test that form is valid when town is not
          completed """
        form = ShopContactInfoForm({
            'shop_phone': 8988980,
            'shop_email': 'test@test.com',
            'shop_street_address1': 'street',
            'shop_street_address2': 'street 2',
            'shop_town': '',
            'shop_county': 'county',
            'shop_country': 'country',
            'shop_postcode': 'postcode',
        })
        self.assertTrue(
            form.is_valid(),
            msg='Form is not valid when phone is town')

    def test_form_is_valid_if_county_is_blank(self):
        """ Test that form is valid when county is not
          completed """
        form = ShopContactInfoForm({
            'shop_phone': 979798,
            'shop_email': 'test@test.com',
            'shop_street_address1': 'street',
            'shop_street_address2': 'street 2',
            'shop_town': 'town',
            'shop_county': '',
            'shop_country': 'country',
            'shop_postcode': 'postcode',
        })
        self.assertTrue(
            form.is_valid(),
            msg='Form is not valid when county is blank')

    def test_form_is_invalid_if_country_is_blank(self):
        """ Test that form is valid when country is not
          completed """
        form = ShopContactInfoForm({
            'shop_phone': 78979879,
            'shop_email': 'test@test.com',
            'shop_street_address1': 'street',
            'shop_street_address2': 'street 2',
            'shop_town': 'town',
            'shop_county': 'county',
            'shop_country': '',
            'shop_postcode': 'postcode',
        })
        self.assertFalse(
            form.is_valid(),
            msg='Form is valid when country is blank')

    def test_form_is_valid_if_postcode_is_blank(self):
        """ Test that form is valid when postcode is not
          completed """
        form = ShopContactInfoForm({
            'shop_phone': 70809,
            'shop_email': 'test@test.com',
            'shop_street_address1': 'street',
            'shop_street_address2': 'street 2',
            'shop_town': 'town',
            'shop_county': 'county',
            'shop_country': 'country',
            'shop_postcode': '',
        })
        self.assertTrue(
            form.is_valid(),
            msg='Form is not valid when postcode is blank')
