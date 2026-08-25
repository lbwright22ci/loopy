
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from core.models import (ShopContactInfo,
                         Announcements, SaleSettings,
                         Postage, UserProfile)
from product.models import (Product, Brand,
                            Thickness, Colour_cat,
                            Colour_var, Shade_Type)

# Create your tests here.


class TestBasketViews(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.shop = ShopContactInfo(
            shop_phone=8988980,
            shop_email='email@email.com'
        )
        cls.shop.save()
        cls.bulk = Announcements(
            bulk_buy=True,
            active=True,
            lower_ball_num=10,
            lower_discount=5,
            upper_discount=20,
            upper_ball_num=10
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

        cls.user = User.objects.create_user(username='testuser',
                                            password='password',
                                            email='test@test.com',
                                            first_name='joe',
                                            last_name='bloggs',
                                            )
        cls.userprofile = UserProfile(
            user=cls.user,
            default_phone=77777777,
            default_street_address1='no street',
            default_town='birmingham',
            wish_list='1',
            temporary_basket={}
        )
        cls.brand1 = Brand(
            name='drops'
        )
        cls.brand1.save()
        cls.thickness1 = Thickness(
            name='DK'
        )
        cls.thickness1.save()
        cls.red = Shade_Type(
            name='red'
        )
        cls.red.save()
        cls.deepred = Colour_cat(
            colour_name='deep red',
            shade_type_id=cls.red
        )
        cls.deepred.save()
        cls.yarn1 = Product(
            brand_id=cls.brand1,
            thickness_id=cls.thickness1,
            name='yarn1',
            price=2.30,
            skein_weight=50,
            sku='YARN1',
            fibre='acrylic',
            visible=True
        )
        cls.yarn1.save()
        cls.redyarn = Colour_var(
            product_id=cls.yarn1,
            colour_cat_id=cls.deepred,
            shade_code=988,
            dye_lot=8989,
        )
        cls.redyarn.save()

    def setUp(self):
        self.client = Client()

    def test_render_basket_view(self):
        """ Verifies request to render empty basket view """
        response = self.client.get(reverse('view_basket'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"There's nothing in your basket yet!", response.content)

    def test_render_basket_view_with_content(self):
        """ Verifies request to render basket view with content"""
        self.client.login(email="test@test.com", password='password')
        session = self.client.session
        session['basket'] = {'1': 6}
        session.save()
        response = self.client.get(reverse('view_basket'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"yarn1", response.content)
        self.assertIn(b"Buy 4 more", response.content)

    def test_update_basket(self):
        """ Verifies request to update basket"""
        self.client.login(email="test@test.com", password='password')
        self.userprofile = UserProfile.objects.get(user__id=self.user.pk)
        session = self.client.session
        session['basket'] = {'1': 6}
        session.save()
        post_data = {
            'quantity': 1,
        }
        response = self.client.post(
            reverse(
                'update_basket',
                args=[1]),
            post_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, expected_url=f'{
                reverse('view_basket')}')
        self.userprofile.refresh_from_db()
        self.assertEqual(self.userprofile.temporary_basket, '{"1": 1}')

    def test_delate_from_basket(self):
        """ Verifies request to delete from basket"""
        self.client.login(email="test@test.com", password='password')
        self.userprofile = UserProfile.objects.get(user__id=self.user.pk)
        session = self.client.session
        session['basket'] = {'1': 6}
        session.save()
        response = self.client.post(reverse('delete_from_basket', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.userprofile.refresh_from_db()
        self.assertEqual(self.userprofile.temporary_basket, '{}')

    def test_add_to_basket(self):
        """ Verifies request to add to basket"""
        self.client.login(email="test@test.com", password='password')
        self.userprofile = UserProfile.objects.get(user__id=self.user.pk)
        session = self.client.session
        session['basket'] = {'1': 6}
        session.save()
        post_data = {
            'quantity': 2,
            'colour_var': 1,
            'redirect_url': f'{reverse('view_basket')}'
        }
        response = self.client.post(reverse('add_to_basket'), post_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, expected_url=f'{
                reverse('view_basket')}')
        self.userprofile.refresh_from_db()
        self.assertEqual(self.userprofile.temporary_basket, '{"1": 8}')
