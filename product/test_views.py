
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


class TestProductViews(TestCase):
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
            wish_list =  '',
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
        cls.pink=Colour_cat(
            colour_name = 'pink',
            shade_type_id = cls.red
        )
        cls.pink.save()
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
        cls.pinkyarn = Colour_var(
            product_id = cls.yarn1,
            colour_cat_id = cls.pink,
            shade_code = 788,
            dye_lot = 899,
            low_stock = True
        )
        cls.pinkyarn.save()

        cls.yarn2 = Product(
            brand_id = cls.brand1,
            thickness_id = cls.thickness1,
            name = 'yarn2',
            price = 2.90,
            skein_weight = 100,
            sku = 'YARN2',
            fibre = 'acrylic',
            visible = True
        )
        cls.yarn2.save()
        cls.redyarn2 = Colour_var(
            product_id = cls.yarn2,
            colour_cat_id = cls.deepred,
            shade_code = 98,
            dye_lot = 8987,
        )
        cls.redyarn2.save()

    def setUp(self):
        self.client = Client()


    def test_all_products_renders_correctly(self):
        """ Test the all products view renders correctly"""
        response = self.client.get(reverse('allproducts'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/all-products.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertIn(b'Find your yarn!', response.content)
        self.assertIn(b'Sort by', response.content)
        self.assertIn(b'Filter', response.content)
        self.assertIn(b'yarn1', response.content)

    def test_product_detail_renders_correctly(self):
        """ Test the product detail view renders correctly"""
        response = self.client.get(reverse('productdetail', args=['drops-yarn1-50']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/product-detail.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertIn(b'Shades available', response.content)
        self.assertIn(b'50g', response.content)
        self.assertIn(b'pink', response.content)
        self.assertIn(b'deep red', response.content)
        self.assertIn(b'2.30', response.content)

    def test_unauthenicated_user_cannot_access_update_wishlist_view(self):
        """ Test that a user who is not logged in cannot access the update wish list view """
        response = self.client.get(reverse('update_wishlist', args=[2]))
        self.assertRedirects(response, expected_url=f"{reverse('account_login')}?next={reverse('update_wishlist', args=[2])}")

    def test_update_wishlist_view_posts(self):
        """ Verify that update wishlist view 
        operates correctly"""
        self.client.login(email = 'test@test.com', password = 'password')
        self.userprofile = UserProfile.objects.get(user__id = self.user.pk)
        response = self.client.post(reverse(
            'update_wishlist', args=[2]))
        self.assertEqual(response.status_code, 200)
        self.userprofile.refresh_from_db()
        self.assertEqual(self.userprofile.wish_list, '2')