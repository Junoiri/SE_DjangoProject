from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from DjangoApp.models import Product
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken


class ProductApiTest(APITestCase):
    def setUp(self):
        self.regular_user = User.objects.create_user(username='testuser', password='testpassword')
        self.admin = User.objects.create_superuser(username='testadmin', password='testpassword')

        self.regular_token = str(AccessToken.for_user(self.regular_user))
        self.admin_token = str(AccessToken.for_user(self.admin))

        self.product = Product.objects.create(name='Temporary Product', price=1.99, available=True)

        self.product_list_url = reverse('product-list')
        self.product_detail_url = reverse('product-detail', kwargs={'pk': self.product.id})

        self.client = APIClient()

    def test_get_all_products_as_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.get(self.product_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_products_as_regular_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.regular_token}')
        response = self.client.get(self.product_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_product_as_regular_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.regular_token}')
        data = {"name": "New Product", "price": 10.00, "available": True}
        response = self.client.post(self.product_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_product_as_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        data = {"name": "New Product", "price": 10.00, "available": True}
        response = self.client.post(self.product_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_product_as_regular_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.regular_token}')
        data = {"name": "Updated Product"}
        response = self.client.patch(self.product_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_product_as_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        data = {"name": "Updated Product"}
        response = self.client.patch(self.product_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_product_as_regular_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.regular_token}')
        response = self.client.delete(self.product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_product_as_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.delete(self.product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_boundary_price_minimum(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        data = {"name": "Boundary Product", "price": 0.01, "available": True}
        response = self.client.post(self.product_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_boundary_price_below_minimum(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        data = {"name": "Boundary Product", "price": 0, "available": True}
        response = self.client.post(self.product_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_name_exceeding_max_length(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        data = {"name": "A" * 256, "price": 10.00, "available": True}
        response = self.client.post(self.product_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
