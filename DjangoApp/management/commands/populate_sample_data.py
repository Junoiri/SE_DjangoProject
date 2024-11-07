from django.core.management.base import BaseCommand
from DjangoApp.models import Product, Customer, Order


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        Product.objects.all().delete()
        Customer.objects.all().delete()
        Order.objects.all().delete()

        product1 = Product.objects.create(
            name='Headset',
            price=59.99,
            available=True
        )
        product2 = Product.objects.create(
            name='Smartphone',
            price=499.99,
            available=True
        )
        product3 = Product.objects.create(
            name='Tablet',
            price=299.99,
            available=False
        )

        customer1 = Customer.objects.create(
            name='Robert Smith',
            address='123 Main St.'
        )
        customer2 = Customer.objects.create(
            name='Mary Johnson',
            address='234 Elm St.'
        )
        customer3 = Customer.objects.create(
            name='Chris Brown',
            address='345 Oak St.'
        )

        order1 = Order.objects.create(
            customer=customer1,
            date='2024-11-06 07:00:00',
            status='New'
        )
        order1.products.add(product1, product2)

        order2 = Order.objects.create(
            customer=customer2,
            date='2024-11-06 08:00:00',
            status='In Process'
        )
        order2.products.add(product2)

        order3 = Order.objects.create(
            customer=customer3,
            date='2024-11-06 09:00:00',
            status='Sent'
        )
        order3.products.add(product1, product3)

        self.stdout.write("Data created successfully.")
