from django.test import TestCase
from DjangoApp.models import Product, Customer, Order
from django.core.exceptions import ValidationError


class ProductModelTest(TestCase):
    def test_create_product_with_valid_data(self):
        temp_product = Product.objects.create(
            name='Temporary product',
            price=1.99,
            available=True
        )
        self.assertEqual(temp_product.name, 'Temporary product')
        self.assertEqual(temp_product.price, 1.99)
        self.assertTrue(temp_product.available)

    def test_create_product_with_negative_price(self):
        with self.assertRaises(ValidationError):
            temp_product = Product(name='Invalid product', price=-1.99, available=True)
            temp_product.full_clean()

    def test_create_product_with_missing_name(self):
        with self.assertRaises(ValidationError):
            temp_product = Product(name='', price=5.00, available=True)
            temp_product.full_clean()

    def test_create_product_with_blank_name(self):
        with self.assertRaises(ValidationError):
            temp_product = Product(name='', price=5.00, available=True)
            temp_product.full_clean()

    def test_create_product_with_edge_case_name_length(self):
        temp_product = Product.objects.create(
            name='A' * 255,
            price=10.00,
            available=True
        )
        self.assertEqual(len(temp_product.name), 255)

    def test_create_product_with_price_exceeding_max(self):
        with self.assertRaises(ValidationError):
            temp_product = Product(name='Expensive product', price=1000000.00, available=True)
            temp_product.full_clean()

    def test_create_product_with_invalid_price_format(self):
        with self.assertRaises(ValidationError):
            temp_product = Product(name='Invalid price format', price=1.999, available=True)
            temp_product.full_clean()


class CustomerModelTest(TestCase):
    def test_create_customer_with_valid_data(self):
        customer = Customer.objects.create(name="John Doe", address="123 Main Street")
        self.assertEqual(customer.name, "John Doe")
        self.assertEqual(customer.address, "123 Main Street")

    def test_create_customer_with_missing_name(self):
        with self.assertRaises(ValidationError):
            customer = Customer(name='', address="123 Main Street")
            customer.full_clean()

    def test_create_customer_with_blank_name(self):
        with self.assertRaises(ValidationError):
            customer = Customer(name='', address="123 Main Street")
            customer.full_clean()

    def test_create_customer_with_missing_address(self):
        with self.assertRaises(ValidationError):
            customer = Customer(name="John Doe", address='')
            customer.full_clean()

    def test_create_customer_with_blank_address(self):
        with self.assertRaises(ValidationError):
            customer = Customer(name="John Doe", address='')
            customer.full_clean()

    def test_create_customer_with_edge_case_name_length(self):
        customer = Customer.objects.create(name="A" * 100, address="123 Main Street")
        self.assertEqual(len(customer.name), 100)

    def test_create_customer_with_name_exceeding_max_length(self):
        with self.assertRaises(ValidationError):
            customer = Customer(name="A" * 101, address="123 Main Street")
            customer.full_clean()

class OrderModelTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(name="John Doe", address="123 Main Street")
        self.product1 = Product.objects.create(name="Product 1", price=10.00, available=True)
        self.product2 = Product.objects.create(name="Product 2", price=15.00, available=False)

    def test_create_order_with_valid_data(self):
        order = Order.objects.create(
            customer=self.customer,
            date="2025-01-01 12:00:00",
            status="New"
        )
        order.products.add(self.product1, self.product2)
        self.assertEqual(order.customer, self.customer)
        self.assertEqual(order.status, "New")
        self.assertEqual(order.products.count(), 2)

    def test_create_order_missing_customer(self):
        with self.assertRaises(ValidationError):
            order = Order(
                customer=None,
                date="2025-01-01 12:00:00",
                status="New"
            )
            order.full_clean()

    def test_create_order_missing_status(self):
        with self.assertRaises(ValidationError):
            order = Order(
                customer=self.customer,
                date="2025-01-01 12:00:00",
                status=None
            )
            order.full_clean()

    def test_create_order_invalid_status(self):
        with self.assertRaises(ValidationError):
            order = Order(
                customer=self.customer,
                date="2025-01-01 12:00:00",
                status="InvalidStatus"
            )
            order.full_clean()

    def test_calculate_total_price_valid_products(self):
        order = Order.objects.create(
            customer=self.customer,
            date="2025-01-01 12:00:00",
            status="New"
        )
        order.products.add(self.product1, self.product2)
        total_price = order.calculate_total_price()
        self.assertEqual(total_price, 25.00)

    def test_calculate_total_price_no_products(self):
        order = Order.objects.create(
            customer=self.customer,
            date="2025-01-01 12:00:00",
            status="New"
        )
        total_price = order.calculate_total_price()
        self.assertEqual(total_price, 0.00)

    def test_can_fulfill_order_with_available_products(self):
        order = Order.objects.create(
            customer=self.customer,
            date="2025-01-01 12:00:00",
            status="New"
        )
        order.products.add(self.product1)
        self.assertTrue(order.can_fulfill_order())

    def test_can_fulfill_order_with_unavailable_products(self):
        order = Order.objects.create(
            customer=self.customer,
            date="2025-01-01 12:00:00",
            status="New"
        )
        order.products.add(self.product1, self.product2)
        self.assertFalse(order.can_fulfill_order())