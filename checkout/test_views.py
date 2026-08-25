
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from core.models import (ShopContactInfo,
                         Announcements, SaleSettings,
                         Postage, UserProfile)
from .forms import ContactAndBillingForm, ShippingAddressForm, SaveDetailsForm
from product.models import (Product, Brand, 
                            Thickness, Colour_cat, 
                            Colour_var, Shade_Type)
from checkout.models import (Order, 
                             YarnOrderLineitem, 
                             ReviewYarns, Shipped)

# Create your tests here.


class TestCheckoutViews(TestCase):
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
            postage_cost=6.50,
            max_no_balls=10,
            max_weight=2
        )
        cls.firstsmall.save()
        cls.firstlarge = Postage(
            postage_class=1,
            parcel_size=1,
            postage_cost=7.50,
            max_no_balls=10,
            max_weight=2
        )
        cls.firstlarge.save()

        cls.user = User.objects.create_user(username = 'testuser',
                                             password='password',
                                             email ='test@test.com',
                                             first_name = 'joe',
                                             last_name = 'bloggs',
        )
        cls.user2 = User.objects.create_user(username = 'testuser2',
                                             password='password2',
                                             email ='try@two.com',
                                             first_name = 'john',
                                             last_name = 'doh',
        )
        cls.superuser = User.objects.create_superuser(username='manager',
                                                      email='man@ager.com',
                                                      password='pass',)
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
            is_shipped = False
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

    def test_render_checkout_stage1_page_nothing_in_basket(self):
        """ Verifies request to render checkout stage 1 content """
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url=f'{reverse('allproducts')}')

    def test_render_checkout_stage1_page_with_items_in_basket_anonymous(self):
        """ Verifies request to render checkout stage 1 content """
        session = self.client.session
        session['basket']={'1': 6}
        session.save()
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'yarn1', response.content)
        self.assertIn(b'13.80', response.content)
        self.assertIn(b'4.50', response.content)
        self.assertIn(b'18.30', response.content)
        self.assertIn(b'Log in', response.content)
        self.assertIsInstance(response.context['form'], ContactAndBillingForm)

    def test_render_checkout_stage1_page_with_items_in_basket_login(self):
        """ Verifies request to render checkout stage 1 content """
        self.client.login(email="test@test.com", password='password')
        self.userprofile = UserProfile.objects.get(user__id = self.user.pk)
        session = self.client.session
        session['basket']={'1': 6}
        session.save()
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'yarn1', response.content)
        self.assertIn(b'13.80', response.content)
        self.assertIn(b'4.50', response.content)
        self.assertIn(b'18.30', response.content)
        self.assertIn(b'bloggs', response.content)
        self.assertIsInstance(response.context['form'], ContactAndBillingForm)

    def test_render_checkout_stage2_page_with_same_shipping_billing(self):
        """ Verifies request to render checkout stage 2 content """
        self.client.login(email="test@test.com", password='password')
        self.userprofile = UserProfile.objects.get(user__id = self.user.pk)
        session = self.client.session
        session['basket']={'1': 6}
        session['bs_same']=True
        session.save()
        response = self.client.get(reverse('checkout-ship'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'yarn1', response.content)
        self.assertIn(b'13.80', response.content)
        self.assertIn(b'4.50', response.content)
        self.assertIn(b'18.30', response.content)
        self.assertIn(b'Second Class', response.content)
        self.assertNotIn(b'Shipping Address', response.content)
        self.assertIsInstance(response.context['form'], ShippingAddressForm)

    def test_render_checkout_stage2_page_with_different_shipping_billing(self):
        """ Verifies request to render checkout stage 2 content """
        self.client.login(email="test@test.com", password='password')
        self.userprofile = UserProfile.objects.get(user__id = self.user.pk)
        session = self.client.session
        session['basket']={'1': 6}
        session['bs_same']=False
        session.save()
        response = self.client.get(reverse('checkout-ship'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'yarn1', response.content)
        self.assertIn(b'13.80', response.content)
        self.assertIn(b'4.50', response.content)
        self.assertIn(b'18.30', response.content)
        self.assertIn(b'Second Class', response.content)
        self.assertIn(b'Shipping Address', response.content)
        self.assertIsInstance(response.context['form'], ShippingAddressForm)

    def test_render_checkout_stage3_page_login(self):
        """ Verifies request to render checkout stage 3 content """
        self.client.login(email="test@test.com", password='password')
        self.userprofile = UserProfile.objects.get(user__id = self.user.pk)
        session = self.client.session
        session['basket']={'1': 6}
        session['first_name']='joe'
        session['second_name']='bloggs'
        session['phone']=80089
        session['email']='test@test.com'
        session['postage_class']=0
        session['is_gift'] = True
        session['gift_message'] = 'gift message added'
        session['billing_street_address1']='street'
        session['shipping_street_address1']='street'
        session['billing_town']='town'
        session['shipping_town']='town'
        session['billing_country']='GB'
        session['billing_postcode']='postcode'
        session.save()
        response = self.client.get(reverse('checkout-final'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'yarn1', response.content)
        self.assertIn(b'13.80', response.content)
        self.assertIn(b'4.50', response.content)
        self.assertIn(b'18.30', response.content)
        self.assertIn(b'2nd Class', response.content)
        self.assertIn(b'gift message added', response.content)
        self.assertIn(b'Shipping Address', response.content)
        self.assertIsInstance(response.context['form'], SaveDetailsForm)

    def test_render_checkout_successpage(self):
        """ Verifies request to render checkout stage 2 content """
        self.client.login(email="test@test.com", password='password')
        self.userprofile = UserProfile.objects.get(user__id = self.user.pk)
        session = self.client.session
        session['basket']={'1': 2}
        session['save_details']= True
        session.save()
        response = self.client.get(reverse('checkout_success', args=[self.order.order_num]))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'A confirmation email will be sent to', response.content)
        self.userprofile.refresh_from_db()
        self.assertEqual(self.userprofile.temporary_basket, '{}')
        self.assertEqual(self.userprofile.user.first_name, 'l')

    def test_checkout_stage1_posts_correctly(self):
        """ test that checkout stage one posts data to session correctly"""
        session = self.client.session
        session['basket']={'1': 2}
        session.save()
        post_data={
            'first_name': 'name1',
            'second_name': 'name2',
            'phone': 77989,
            'email':'test@test.com',
            'billing_street_address1' : 'street',
            'billing_street_address2' : 'street 2',
            'billing_town' : 'town',
            'billing_county' : 'county',
            'billing_country' : 'GB',
            'billing_postcode' : 'postcode',
            'billing_shipping_same' : True
        }
        response = self.client.post(reverse('checkout'), post_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url=f'{reverse('checkout-ship')}')

    def test_checkout_stage2_posts_correctly(self):
        """ test that checkout stage 2 posts data to session correctly"""
        session = self.client.session
        session['basket']={'1': 2}
        session['bs_same']=False
        session.save()
        post_data={
            'shipping_street_address1' : 'street',
            'shipping_street_address2' : 'street 2',
            'shipping_town' : 'town',
            'shipping_county' : 'county',
            'shipping_country' : 'GB',
            'shipping_postcode' : 'postcode',
            'shippingClass': '0',
            'is_gift':'on',
            'gift_message':'this is a gift message'
        }
        response = self.client.post(reverse('checkout-ship'), post_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url=f'{reverse('checkout-final')}')

    def test_checkout_stage3_posts_correctly(self):
        """ test that checkout stage 3 posts data to session correctly"""
        session = self.client.session
        session['basket']={'1': 6}
        session['first_name']='joe'
        session['second_name']='bloggs'
        session['phone']=80089
        session['email']='test@test.com'
        session['postage_class']=0
        session['is_gift'] = True
        session['gift_message'] = 'gift message added'
        session['billing_street_address1']='street'
        session['shipping_street_address1']='street'
        session['billing_town']='town'
        session['shipping_town']='town'
        session['billing_country']='GB'
        session['billing_postcode']='postcode'
        session['billing_county']='county',
        session['shipping_county']='county',
        session['shipping_country']='GB',
        session['shipping_postcode']='postcode'
        session.save()
        post_data={
            'save_details':True,
            'client_secret':'809090_secret80980809'
        }
        response = self.client.post(reverse('checkout-final'), post_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Order.objects.all().count(), 2)
        new_order = Order.objects.get(pk=2)
        new_order_num = new_order.order_num
        self.assertRedirects(response, expected_url=f'{reverse('checkout_success', args=[new_order_num])}')

    def test_unauthenticated_user_cannot_access_cancel_order_view(self):
        """ Test that a user who is not logged in cannot access cancel order view """
        post_data={
            'amount': 4.60,
            'stripe_pid': 'hjkhi98098980bhjbjh',
            'reason': 'customer cancelled order'
        }
        response = self.client.post(reverse('cancel_order', args=[self.order.order_num]), post_data)
        self.assertRedirects(response, expected_url=f"{reverse('account_login')}?next={reverse('cancel_order', args=[self.order.order_num])}")

    def test_different_authenticated_user_cannot_access_cancel_order_view_of_another_customer(self):
        """ Test that a logged in user in cannot access cancel order view of someone else's order """
        self.client.login(email="try@two.com", password='password2')
        post_data={
            'amount': 4.60,
            'stripe_pid': 'hjkhi98098980bhjbjh',
            'reason': 'customer cancelled order'
        }
        response = self.client.post(reverse('cancel_order', args=[self.order.order_num]), post_data)
        self.assertRedirects(response, expected_url=f"{reverse('home')}")

    def test_only_superuser_can_access_shipped_view(self):
        """ Test that only superuser can access shipped view """
        self.client.login(email="test@test.com", password='password')
        post_data={
            'order': '1',
        }
        response = self.client.post(reverse('mark_shipped'), post_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url=f'{reverse('home')}')

    def test_superuser_can_mar_order_as_shipped(self):
        """ Test that superuser can access shipped view """
        self.client.login(email="man@ager.com", password='pass')
        post_data={
            'order': '1',
        }
        response = self.client.post(reverse('mark_shipped'), post_data)
        self.order.refresh_from_db()
        self.assertEqual(self.order.is_shipped, True)
        self.assertEqual(Shipped.objects.all().count(), 1)
        self.assertEqual(response.status_code, 302)