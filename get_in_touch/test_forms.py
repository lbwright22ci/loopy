from django.test import TestCase
from .forms import ContactForm

# Create your tests here.


class TestContactForm(TestCase):

    def test_form_is_valid(self):
        """ Test that form is valid when all fields are
          completed """
        form = ContactForm({
            'name': 'name',
            'email': 'test@test.com',
            'subject': 0,
            'message': 'Hello!'
        })
        self.assertTrue(form.is_valid(), msg='Form is not valid')

    def test_form_is_invalid_if_name_is_blank(self):
        """ Test that form is declared invalid if name is not
          completed """
        form = ContactForm({
            'name': '',
            'email': 'test@test.com',
            'message': 'Hello!',
            'subject': 0
        })
        self.assertFalse(
            form.is_valid(), msg='Form is valid when name is blank')

    def test_form_is_invalid_if_email_is_blank(self):
        """ Test that form is declared invalid if email is not completed"""
        form = ContactForm({
            'name': 'name',
            'email': '',
            'message': 'Hello!',
            'subject': 0
        })
        self.assertFalse(
            form.is_valid(), msg='Form is valid when email is blank')

    def test_form_is_invalid_if_comment_is_blank(self):
        """ Test that form is declared invalid if message is not
        completed"""
        form = ContactForm({
            'name': 'name',
            'email': 'test@test.com',
            'message': '',
            'subject': 0
        })
        self.assertFalse(
            form.is_valid(), msg='Form is valid when message is blank')

    def test_form_is_invalid_if_subject_is_blank(self):
        """ Test that form is declared invalid if subject is not
        completed"""
        form = ContactForm({
            'name': 'name',
            'email': 'test@test.com',
            'message': 'hello!',
            'subject': ''
        })
        self.assertFalse(
            form.is_valid(), msg='Form is valid when subject is blank')

    def test_form_is_invalid_if_subject_is_not_in_range(self):
        """ Test that form is declared invalid if subject is not
        in range"""
        form = ContactForm({
            'name': 'name',
            'email': 'test@test.com',
            'message': '',
            'subject': 7
        })
        self.assertFalse(
            form.is_valid(), msg='Form is valid when subject is not in range')
