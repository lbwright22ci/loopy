from pathlib import Path
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .models import (HomePageSlides, ShopContactInfo,
                         Announcements, SaleSettings,
                         Postage, UserProfile)
from .forms import DetailsForm, AddressForm

# Create your tests here.


class TestHomeViews(TestCase):
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
        self.user = User.objects.create_user(username = 'testuser',
                                             password='password',
                                             email ='test@test.com',
        )
        self.userprofile = UserProfile(
            user= self.user,
            wish_list = '1 2 3',
        )

    def test_render_home_page(self):
        """ Verifies request to render Home page content """
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Loopy", response.content)
        self.assertIn(b"phone", response.content)
        
    def test_render_account_home(self):
        """ Verifies request to render account home page content"""
        self.client.login(email = 'test@test.com', password = 'password')
        response = self.client.get(reverse('customer_account'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'My orders', response.content)
        self.assertIn(b'My favourites', response.content)
        self.assertIsInstance(response.context['address_form'], AddressForm)
        self.assertIsInstance(response.context['details_form'], DetailsForm)
    