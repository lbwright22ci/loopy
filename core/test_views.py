from pathlib import Path
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from .models import (HomePageSlides, ShopContactInfo,
                         Announcements, SaleSettings,
                         Postage, UserProfile)
from .forms import DetailsForm, AddressForm
from product.models import (Product, Brand, 
                            Thickness, Colour_cat, 
                            Colour_var, Shade_Type)
from checkout.models import (Order, 
                             YarnOrderLineitem, 
                             ReviewYarns)

# Create your tests here.


class TestHomeViews(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.shop = ShopContactInfo(
            shop_phone=8988980,
            shop_email='email@email.com'
        )
        cls.shop.save()
        cls.bulk = Announcements(
            bulk_buy=False,
            active=True,
            lower_ball_num=10,
            lower_discount=10,
            upper_discount=20,
            upper_ball_num=20
        )
        cls.bulk.save()
        cls.sale = SaleSettings(
            sale_percent=20,
            active=True
        )
        cls.sale.save()
        cls.secondsmall = Postage(
            postage_class=0,
            parcel_size=0,
            postage_cost=4.50,
            max_no_balls=10,
            max_weight=2
        )
        cls.secondsmall.save()
        cls.secondlarge = Postage(
            postage_class=0,
            parcel_size=1,
            postage_cost=5.50,
            max_no_balls=10,
            max_weight=2
        )
        cls.secondlarge.save()
        cls.firstsmall = Postage(
            postage_class=1,
            parcel_size=0,
            postage_cost=4.50,
            max_no_balls=10,
            max_weight=2
        )
        cls.firstsmall.save()
        cls.firstlarge = Postage(
            postage_class=1,
            parcel_size=1,
            postage_cost=5.50,
            max_no_balls=10,
            max_weight=2
        )
        cls.firstlarge.save()
        cls.test_image_path = (
            Path(__file__).resolve().parent.parent /
            "static/images/balls-in-a-line.png")
        cls.slide1 = HomePageSlides.objects.create(
            title='loopy',
            subtitle='some text',
            alt_text='alt text',
        )

        cls.slide2 = HomePageSlides(
            title='loopy 2',
            subtitle='some text',
            alt_text='alt text',

        )
        cls.slide2.save()
        cls.slide3 = HomePageSlides(
            title='loopy 3',
            subtitle='some text',
            alt_text='alt text',

        )
        cls.slide3.save()
        cls.slide4 = HomePageSlides(
            title='loopy4',
            subtitle='some text',
            alt_text='alt text',

        )
        cls.slide4.save()
        cls.slide5 = HomePageSlides(
            title='loopy5',
            subtitle='some text',
            alt_text='alt text',

        )
        cls.slide5.save()
        cls.user = User.objects.create_user(username = 'testuser',
                                             password='password',
                                             email ='test@test.com',
                                             first_name = 'joe',
                                             last_name = 'bloggs',
        )
        cls.userprofile = UserProfile(
            user= cls.user,
            default_phone = 77777777,
            default_street_address1 = 'no street',
            default_town = 'birmingham',
            wish_list = '1',
        )
        cls.brand1= Brand(
            name = 'drops'
        )
        cls.brand1.save()
        cls.thickness1=Thickness(
            name = 'DK'
        )
        cls.thickness1.save()
        cls.red = Shade_Type(
            name = 'red'
        )
        cls.red.save()
        cls.deepred=Colour_cat(
            colour_name = 'deep red',
            shade_type_id = cls.red
        )
        cls.deepred.save()
        cls.yarn1 = Product(
            brand_id = cls.brand1,
            thickness_id = cls.thickness1,
            name = 'yarn1',
            price = 2.30,
            skein_weight = 50,
            sku = 'YARN1',
            fibre = 'acrylic',
            visible = True
        )
        cls.yarn1.save()
        cls.redyarn = Colour_var(
            product_id = cls.yarn1,
            colour_cat_id = cls.deepred,
            shade_code = 988,
            dye_lot = 8989,
        )
        cls.redyarn.save()
        cls.order = Order.objects.create(
            user_profile = cls.userprofile.pk,
            first_name = 'l',
            second_name = 'w',
            email = 'test@order.com',
            phone = 888,
            billing_street_address1= 'street1',
            billing_town = 'town',
            billing_county = 'county',
            billing_postcode = 'postcode',
            billing_country ='GB',
            shipping_street_address1= 'street1',
            shipping_town = 'town',
            shipping_county = 'county',
            shipping_postcode = 'postcode',
            shipping_country ='GB',
            stripe_pid = 'hjkhi98098980bhjbjh',
            order_num = 'order_num2',
            is_shipped = True
        )
        
        cls.line = YarnOrderLineitem(
            order = cls.order,
            yarn = cls.redyarn,
            quantity = 2
        )
        cls.line.save()
        cls.reviewred = ReviewYarns(
            order = cls.order,
            yarn = cls.redyarn,
            rating = 4,
            comment = 'comment',
            approved = True
        )
        cls.reviewred.save()

    def setUp(self):
        self.client = Client()

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

    def test_unauthenticated_user_cannot_access_acount_page(self):
        """ Test that a usre who is not logged in cannot access the account page """
        response = self.client.get(reverse('customer_account'))
        self.assertRedirects(response, expected_url=f"{reverse('account_login')}?next={reverse('customer_account')}")

    def test_update_details_account_home(self):
        """ Verify that updating details via form on account page 
        operates correctly"""
        self.client.login(email = 'test@test.com', password = 'password')
        self.userprofile = UserProfile.objects.get(user__id = self.user.pk)
        post_data = {
            'first_name ': 'name 1',
            'last_name' : 'name 2',
            'Phone': 999
        }
        response = self.client.post(reverse(
            'update_details'), post_data)
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.userprofile.refresh_from_db()
        self.assertEqual(self.userprofile.user.first_name, 'name 1')
        self.assertNotEqual(self.user.last_name, 'bloggs')
        self.assertEqual(self.userprofile.default_phone, 999)

    def test_unauthenticated_user_cannot_access_update_details_view(self):
        """ Test that a usre who is not logged in cannot update customer details """
        self.userprofile = UserProfile.objects.get(user__id = 1)
        post_data = {
            'first_name ': 'name 1',
            'last_name' : 'name 2',
            'Phone': 999
        }
        response = self.client.post(reverse('update_details'), post_data)
        self.assertRedirects(response, expected_url=f"{reverse('account_login')}?next={reverse('update_details')}")

    def test_update_address_account_home(self):
        """ Verify that updating address via form on account page 
        operates correctly"""
        self.client.login(email = 'test@test.com', password = 'password')
        self.userprofile = UserProfile.objects.get(user__id = self.user.pk)
        post_data = {
            'default_street_address1': 'some street',
        }
        response = self.client.post(reverse(
            'update_address'), post_data)
        self.assertEqual(response.status_code, 302)
        self.userprofile.refresh_from_db()
        self.assertEqual(self.userprofile.default_street_address1, 'some street')
        self.assertNotEqual(self.userprofile.default_street_address1, 'no street')

    def test_unauthenticated_user_cannot_update_address(self):
        """ Test that a usre who is not logged in cannot update customer default address details """
        self.userprofile = UserProfile.objects.get(user__id = 1)
        post_data = {
            'default_street_address1': 'some street',
        }
        response = self.client.post(reverse('update_address'), post_data)
        self.assertRedirects(response, expected_url=f"{reverse('account_login')}?next={reverse('update_address')}")

    def test_past_order_page_renders(self):
        """ Test that past order page renders correctly """
        self.client.login(email = 'test@test.com', password = 'password')
        self.userprofile = UserProfile.objects.get(user__id = self.user.pk)
        response = self.client.get(reverse('past_order', args=[self.order.order_num]))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Shipping Address', response.content)
        self.assertIn(b'988', response.content)

    def test_unauthenticated_user_cannot_view_past_order(self):
        """ Test that a usre who is not logged in cannot view past order """
        response = self.client.get(reverse('past_order', args=[self.order.order_num]))
        self.assertRedirects(response, expected_url=f"{reverse('account_login')}?next={reverse('past_order', args=[self.order.order_num])}")

    def test_leave_review_page_renders(self):
        """ Test that leave review page renders correctly """
        self.client.login(email = 'test@test.com', password = 'password')
        self.userprofile = UserProfile.objects.get(user__id = self.user.pk)
        response = self.client.get(reverse('leave_review', args=[self.order.order_num]))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"We'd love to hear what you think", response.content)
        self.assertIn(b'rating', response.content)

    def test_unauthenticated_user_cannot_view_leave_review_page(self):
        """ Test that a usre who is not logged in cannot view leave review page """
        response = self.client.get(reverse('leave_review', args=[self.order.order_num]))
        self.assertRedirects(response, expected_url=f"{reverse('account_login')}?next={reverse('leave_review', args=[self.order.order_num])}")


    def test_submit_review(self):
        """ test submit review"""
        self.client.login(email = 'test@test.com', password = 'password')
        self.userprofile = UserProfile.objects.get(user__id = self.user.pk)
        self.reviewred = ReviewYarns.objects.get(order = self.order)
        post_data ={
            'rating': 2,
            'comment' : 'new comment',
            'yarn': self.redyarn.id
        }
        response = self.client.post(reverse('submit_review', args=[self.order.order_num]), post_data)
        self.assertEqual(response.status_code, 200)
        self.reviewred.refresh_from_db()
        self.assertEqual(ReviewYarns.objects.all().count(), 1)
        self.assertNotEqual(self.reviewred.approved, True)
        self.assertEqual(self.reviewred.rating, 2)

    def test_unauthenticated_user_cannot_leave_feedback(self):
        """ Test that a usre who is not logged in cannot update or submit feedback """
        self.userprofile = UserProfile.objects.get(user__id = 1)
        self.reviewred = ReviewYarns.objects.get(order = self.order)
        post_data ={
            'rating': 2,
            'comment' : 'new comment',
            'yarn': self.redyarn.id
        }
        response = self.client.post(reverse('submit_review', args=[self.order.order_num]), post_data)
        self.assertRedirects(response, expected_url=f"{reverse('account_login')}?next={reverse('submit_review', args=[self.order.order_num])}")
