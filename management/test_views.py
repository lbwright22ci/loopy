
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from core.models import (ShopContactInfo,
                         Announcements, SaleSettings,
                         Postage, UserProfile)
from .forms import ShopContactInfoForm
from product.models import (Product, Brand,
                            Thickness, Colour_cat,
                            Colour_var, Shade_Type)
from checkout.models import (Order,
                             YarnOrderLineitem)

# Create your tests here.


class TestManagementViews(TestCase):
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
        cls.user = User.objects.create_user(username='testuser',
                                            password='password',
                                            email='test@test.com',
                                            first_name='joe',
                                            last_name='bloggs',
                                            )
        cls.user2 = User.objects.create_user(username='testuser2',
                                             password='password2',
                                             email='try@two.com',
                                             first_name='john',
                                             last_name='doh',
                                             )
        cls.superuser = User.objects.create_superuser(username='manager',
                                                      email='man@ager.com',
                                                      password='pass',)
        cls.userprofile = UserProfile(
            user=cls.user,
            default_phone=77777777,
            default_street_address1='no street',
            default_town='birmingham',
            wish_list='1',
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
        cls.order = Order.objects.create(
            user_profile=cls.userprofile.pk,
            first_name='l',
            second_name='w',
            email='test@order.com',
            phone=888,
            billing_street_address1='street1',
            billing_town='town',
            billing_county='county',
            billing_postcode='postcode',
            billing_country='GB',
            shipping_street_address1='street1',
            shipping_town='town',
            shipping_county='county',
            shipping_postcode='postcode',
            shipping_country='GB',
            stripe_pid='hjkhi98098980bhjbjh',
            order_num='order_num2',
            is_shipped=True
        )

        cls.line = YarnOrderLineitem(
            order=cls.order,
            yarn=cls.redyarn,
            quantity=2
        )
        cls.line.save()

    def setUp(self):
        self.client = Client()

    def test_unauthenicated_user_cannot_access_management_page(self):
        """ Test that a user who is not logged in cannot access the management home page """
        response = self.client.get(reverse('management_home'))
        self.assertRedirects(
            response, expected_url=f"{
                reverse('account_login')}?next={
                reverse('management_home')}")

    def test_non_super_user_cannot_access_management_page(self):
        """ Test that a none super user cannot access the management home page """
        self.client.login(email='test@test.com', password='password')
        response = self.client.get(reverse('management_home'))
        self.assertRedirects(response, expected_url=f"{reverse('home')}")

    def test_super_user_can_access_management_page_and_renders_correctly(self):
        """ Test that a super user can access the management home page and it renders correctly"""
        self.client.login(email='man@ager.com', password='pass')
        response = self.client.get(reverse('management_home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'management/admin-home.html')
        self.assertTemplateNotUsed(response, 'base.html')
        self.assertIn(b'Dashboard', response.content)
        self.assertIn(b'Shop Settings', response.content)

    def test_unauthenicated_user_cannot_access_management_settings(self):
        """ Test that a user who is not logged in cannot access the management settings page """
        response = self.client.get(reverse('management_settings'))
        self.assertRedirects(
            response, expected_url=f"{
                reverse('account_login')}?next={
                reverse('management_settings')}")

    def test_non_super_user_cannot_access_management_settings(self):
        """ Test that a none super user cannot access the management settings page """
        self.client.login(email='test@test.com', password='password')
        response = self.client.get(reverse('management_settings'))
        self.assertRedirects(response, expected_url=f"{reverse('home')}")

    def test_super_user_can_access_management_settings_and_renders_correctly(
            self):
        """ Test that a super user can access the management settings page and it renders correctly"""
        self.client.login(email='man@ager.com', password='pass')
        response = self.client.get(reverse('management_settings'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'management/admin-settings.html')
        self.assertTemplateNotUsed(response, 'base.html')
        self.assertIsInstance(
            response.context['shop_form'],
            ShopContactInfoForm)
        self.assertIn(b'Sale Settings', response.content)
        self.assertIn(b'Promotions', response.content)

    def test_unauthenicated_user_cannot_access_management_orders(self):
        """ Test that a user who is not logged in cannot access the management orders page """
        response = self.client.get(reverse('management_orders'))
        self.assertRedirects(
            response, expected_url=f"{
                reverse('account_login')}?next={
                reverse('management_orders')}")

    def test_non_super_user_cannot_access_management_orders(self):
        """ Test that a none super user cannot access the management orders page """
        self.client.login(email='test@test.com', password='password')
        response = self.client.get(reverse('management_orders'))
        self.assertRedirects(response, expected_url=f"{reverse('home')}")

    def test_super_user_can_access_management_orders_page_and_renders_correctly(
            self):
        """ Test that a super user can access the management orders page and it renders correctly"""
        self.client.login(email='man@ager.com', password='pass')
        response = self.client.get(reverse('management_orders'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'management/admin-orders.html')
        self.assertTemplateNotUsed(response, 'base.html')
        self.assertIn(b'order_num2', response.content)
        self.assertIn(b'Refunded', response.content)

    def test_unauthenicated_user_cannot_access_update_shopsettings_view(self):
        """ Test that a user who is not logged in cannot access the update shop settings view """
        response = self.client.get(reverse('update_shopsettings'))
        self.assertRedirects(
            response, expected_url=f"{
                reverse('account_login')}?next={
                reverse('update_shopsettings')}")

    def test_non_super_user_cannot_access_update_shopsettings_view(self):
        """ Test that a none super user cannot access the update shop settings view """
        self.client.login(email='test@test.com', password='password')
        response = self.client.get(reverse('update_shopsettings'))
        self.assertRedirects(response, expected_url=f"{reverse('home')}")

    def test_unauthenicated_user_cannot_access_update_salesettings_view(self):
        """ Test that a user who is not logged in cannot access the update sale settings view """
        response = self.client.get(reverse('update_salesettings'))
        self.assertRedirects(
            response, expected_url=f"{
                reverse('account_login')}?next={
                reverse('update_salesettings')}")

    def test_non_super_user_cannot_access_update_salesettings_view(self):
        """ Test that a none super user cannot access the update sale settings view """
        self.client.login(email='test@test.com', password='password')
        response = self.client.get(reverse('update_salesettings'))
        self.assertRedirects(response, expected_url=f"{reverse('home')}")

    def test_unauthenicated_user_cannot_access_update_announcements_view(self):
        """ Test that a user who is not logged in cannot access the update announcements view """
        response = self.client.get(reverse('update_announcements'))
        self.assertRedirects(
            response, expected_url=f"{
                reverse('account_login')}?next={
                reverse('update_announcements')}")

    def test_non_super_user_cannot_access_update_announcements_view(self):
        """ Test that a none super user cannot access the update announcements view """
        self.client.login(email='test@test.com', password='password')
        response = self.client.get(reverse('update_announcements'))
        self.assertRedirects(response, expected_url=f"{reverse('home')}")

    def test_update_shopsettings_view_posts(self):
        """ Verify that update shop settings view
        operates correctly"""
        self.client.login(email='man@ager.com', password='pass')
        self.shop = ShopContactInfo.objects.all()[0]
        post_data = {
            'shop_phone': 7777,
            'shop_email': 'new@email.com',
            'shop_street_address1': 'new address',
            'shop_street_address2': '',
            'shop_town': 'town',
            'shop_county': 'county',
            'shop_country': 'GB',
            'shop_postcode': 'NEW 123'
        }
        response = self.client.post(reverse(
            'update_shopsettings'), post_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, expected_url=f'{
                reverse('management_settings')}')
        self.shop.refresh_from_db()
        self.assertEqual(self.shop.shop_phone, 7777)
        self.assertNotEqual(self.shop.shop_email, 'email@email.com')
        self.assertEqual(self.shop.shop_postcode, 'NEW 123')
        self.assertEqual(self.shop.shop_street_address1, 'new address')

    def test_update_salesettings_view_posts(self):
        """ Verify that update sale settings view
        operates correctly"""
        self.client.login(email='man@ager.com', password='pass')
        self.sale = SaleSettings.objects.get(sale_percent=20)
        post_data = {
            'sale_percent': 5,
        }
        response = self.client.post(reverse(
            'update_salesettings'), post_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, expected_url=f'{
                reverse('management_settings')}')
        self.sale.refresh_from_db()
        self.assertEqual(self.sale.sale_percent, 5)
        self.assertEqual(self.sale.active, True)

    def test_update_announcements_view_posts(self):
        """ Verify that update announcement view
        operates correctly"""
        self.client.login(email='man@ager.com', password='pass')
        self.bulk = Announcements.objects.get(lower_ball_num=10)
        post_data = {
            'bulk_buy': True,
            'lower_ball_num': 0,
            'upper_ball_num': 30,
            'lower_discount': 0,
            'upper_discount': 15
        }
        response = self.client.post(reverse(
            'update_announcements'), post_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, expected_url=f'{
                reverse('management_settings')}')
        self.bulk.refresh_from_db()
        self.assertEqual(self.bulk.upper_ball_num, 30)
        self.assertNotEqual(self.bulk.lower_ball_num, 10)
        self.assertEqual(self.bulk.bulk_buy, True)
        self.assertEqual(self.bulk.upper_discount, 15)
