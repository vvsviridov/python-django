from string import ascii_letters
from random import choices

from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth.models import User, Permission
from django.conf import settings

from .models import Product, Order



class ProductCreateViewTestCase(TestCase):
    def setUp(self):
        self.product_name = ''.join(choices(ascii_letters, k=10))
        Product.objects.filter(name=self.product_name).delete()
        password = 'password123'
        self.user = User.objects.create_user(
            username='test_user', password=password)
        permission = Permission.objects.get(codename='add_product')
        self.user.user_permissions.add(permission)
        self.client.login(username='test_user', password=password)

    def test_create_product(self):
        response = self.client.post(
            reverse('shopapp:product_create'),
            {
                'name': self.product_name,
                'price': '123.45',
                'description': 'A good table',
                'discount': '3',
            }
        )
        self.assertRedirects(response, reverse('shopapp:products_list'))
        self.assertTrue(
            Product.objects.filter(name=self.product_name).exists())


class ProductDetailsViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        password = 'password123'
        cls.user = User.objects.create_user(
            username='test_user', password=password)
        cls.product = Product.objects.create(
            name=''.join(choices(ascii_letters, k=10)),
            created_by=cls.user
        )

    @classmethod
    def tearDownClass(cls):
        cls.product.delete()
        cls.user.delete()

    def test_create_product(self):
        response = self.client.get(
            reverse('shopapp:product_details', kwargs={'pk': self.product.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_create_product_and_check_content(self):
        response = self.client.get(
            reverse('shopapp:product_details', kwargs={'pk': self.product.pk})
        )
        self.assertContains(response, self.product.name)


class ProductsListViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        password = 'password123'
        cls.user = User.objects.create_user(
            username='test_user', password=password)
    
    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    fixtures = ['products-fixture.json']

    def test_products(self):
        response = response = self.client.get(reverse('shopapp:products_list'))
        for product in Product.objects.filter(archived=False):
            self.assertContains(response, product.name)

    def test_products_context(self):
        response = response = self.client.get(reverse('shopapp:products_list'))
        products = Product.objects.filter(archived=False)
        products_ = response.context['products']
        for p, p_ in zip(products, products_):
            self.assertEqual(p.pk, p_.pk)

    def test_products_queryset(self):
        response = response = self.client.get(reverse('shopapp:products_list'))
        products_ = response.context['products']
        self.assertQuerySetEqual(
            qs=Product.objects.filter(archived=False).all(),
            values=[p.pk for p in response.context['products']],
            transform=lambda p: p.pk,
        )
        self.assertTemplateUsed(response, 'shopapp/products-list.html')


class OrdersListViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(
            username='test_user', password='password123')
    
    def setUp(self):
        self.client.force_login(self.user)
    
    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
    
    def test_orders_view(self):
        response = self.client.get(reverse('shopapp:orders_list'))
        self.assertContains(response, 'Orders')
    
    def test_orders_view_not_auth(self):
        self.client.logout()
        response = self.client.get(reverse('shopapp:orders_list'))
        # self.assertRedirects(response, str(settings.LOGIN_URL))
        self.assertEqual(response.status_code, 302)
        self.assertIn(str(settings.LOGIN_URL), response.url)


class ProductsExportViewTestCase(TestCase):
    fixtures = ['products-fixture.json']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.client.force_login(self.user)

    def test_get_products_view(self):
        response = self.client.get(reverse('shopapp:products-export'))
        self.assertEqual(response.status_code, 200)
        products = Product.objects.order_by('pk').all()
        expected_data = [
            {
                'pk': p.pk,
                'name': p.name,
                'price': str(p.price),
                'archived': p.archived,
                'created_by': p.created_by.pk,
            }
            for p in products
        ]
        products_data = response.json()
        self.assertEqual(
            products_data['products'],
            expected_data
        )
        print('Response products: ', products_data['products'])
        print('Expected data: ', expected_data)

class OrderDetailsViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(
            username='test_user', password='password123')
        permission = Permission.objects.get(codename='view_order')
        cls.user.user_permissions.add(permission)

    def setUp(self):
        self.client.force_login(self.user)
        self.order = Order.objects.create(
            user=self.user,
            delivery_address="Pushkina St. 17-99",
            promocode="IREMEMBER",
        )

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
    
    def tearDown(self):
        self.order.delete()

    def test_order_details(self):
        response = self.client.get(
            reverse('shopapp:order_details', kwargs={'pk': self.order.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.order.delivery_address)
        self.assertContains(response, self.order.promocode)
        ctx_order = response.context['order']
        self.assertEqual(ctx_order.pk, self.order.pk)


class OrdersExportViewTestCase(TestCase):
    fixtures = [
        'products-fixture.json',
        'orders-fixture.json',
    ]

    def test_get_orders_view(self):
        response = self.client.get(reverse('shopapp:orders-export'))
        self.assertEqual(response.status_code, 200)
        orders = Order.objects.order_by('pk').all()
        expected_data = [
            {
                'pk': o.pk,
                'delivery_address': o.delivery_address,
                'promocode': o.promocode,
                'user': o.user.pk,
                'products': [p.pk for p in o.products.all()],
            }
            for o in orders
        ]
        orders_data = response.json()
        self.assertEqual(
            orders_data['orders'],
            expected_data
        )
        print('Response orders: ', orders_data['orders'])
        print('Expected data: ', expected_data)
