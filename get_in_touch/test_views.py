from pathlib import Path
from django.test import TestCase
from django.urls import reverse
from .forms import ContactForm
from core.models import (HomePageSlides, ShopContactInfo,
                         Announcements, SaleSettings,
                         Postage)

# Create your tests here.


class TestContactViews(TestCase):
    def setUp(self):
        self.shop = ShopContactInfo(
            shop_phone=8988980,
            shop_email='email@email.com'
        )
        self.shop.save()
        self.bulk = Announcements(
            bulk_buy=False,
            active=True,
            lower_ball_num=10,
            lower_discount=10,
            upper_discount=20,
            upper_ball_num=20
        )
        self.bulk.save()
        self.sale = SaleSettings(
            sale_percent=20,
            active=True
        )
        self.sale.save()
        self.secondsmall = Postage(
            postage_class=0,
            parcel_size=0,
            postage_cost=4.50,
            max_no_balls=10,
            max_weight=2
        )
        self.secondsmall.save()
        self.secondlarge = Postage(
            postage_class=0,
            parcel_size=1,
            postage_cost=5.50,
            max_no_balls=10,
            max_weight=2
        )
        self.secondlarge.save()
        self.firstsmall = Postage(
            postage_class=1,
            parcel_size=0,
            postage_cost=4.50,
            max_no_balls=10,
            max_weight=2
        )
        self.firstsmall.save()
        self.firstlarge = Postage(
            postage_class=1,
            parcel_size=1,
            postage_cost=5.50,
            max_no_balls=10,
            max_weight=2
        )
        self.firstlarge.save()
        self.test_image_path = (
            Path(__file__).resolve().parent.parent /
            "static/images/balls-in-a-line.png")
        self.slide1 = HomePageSlides.objects.create(
            title='loopy',
            subtitle='some text',
            alt_text='alt text',
        )

        self.slide2 = HomePageSlides(
            title='loopy 2',
            subtitle='some text',
            alt_text='alt text',

        )
        self.slide2.save()
        self.slide3 = HomePageSlides(
            title='loopy 3',
            subtitle='some text',
            alt_text='alt text',

        )
        self.slide3.save()
        self.slide4 = HomePageSlides(
            title='loopy4',
            subtitle='some text',
            alt_text='alt text',

        )
        self.slide4.save()
        self.slide5 = HomePageSlides(
            title='loopy5',
            subtitle='some text',
            alt_text='alt text',

        )
        self.slide5.save()

    def test_render_contact_page_with_contact_form(self):
        """ Verifies request to render Contact page content containing the
          contact form """
        response = self.client.get(reverse('contact_page'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Get in touch!", response.content)
        self.assertIn(b"If you have a query about a product", response.content)
        self.assertIsInstance(response.context['form'], ContactForm)

    def test_successful_contact_form_submission(self):
        """Test for posting a contact us request on the contact page"""
        post_data = {
            'name': 'name', 'email': 'test@test.com',
            'subject': 0,
            'message': 'get in touch'
        }
        response = self.client.post(reverse(
            'contact_page'), post_data)
        self.assertEqual(response.status_code, 302)

        self.assertRedirects(
            response,
            '/yarns/',
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True)
