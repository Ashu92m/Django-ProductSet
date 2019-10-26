from django.test import TestCase

# Create your tests here.
import os.path
from django.conf import settings

from rest_framework.test import APITestCase

from ProductDetail.models import Product, Metric, Issue


class MetricCreateTestCase(APITestCase):
    def test_create_metric(self):
        initial_product_count = Metric.objects.count()
        metric_attrs = {
            'title': 'Metric 10',
            'description': 'Metric Number 10',
        }
        response = self.client.post('/api/v1/metric/new', metric_attrs)

        metric_attrs = {
            'title': 'Metric 12',
            'description': 'Metric Number 11',
        }
        response = self.client.post('/api/v1/metric/new', metric_attrs)

        metric_attrs = {
            'title': 'Metric 13',
            'description': 'Metric Number 13',
        }
        response = self.client.post('/api/v1/metric/new', metric_attrs)

        self.assertEqual(
            Metric.objects.count(),
            initial_product_count + 3,
        )

class MetricUpdateTestCase(APITestCase):
    def test_update_metric(self):
        metric = Metric.objects.get(title='Metric 12')
        response = self.client.patch(
            '/api/v1/products/{}/'.format(metric.id),
            {
                'title': 'Metric 12',
                'description': 'Metric Number 12',
            },
            format='json',
        )
        updated = metric.objects.get(id=metric.id)
        self.assertEqual(updated.description, 'Metric Number 12')
        
class MetricDestroyTestCase(APITestCase):
    def test_delete_metric(self):
        initial_metric_count = Metric.objects.count()
        metric_id = Metric.objects.get(title='Metric 13').id
        self.client.delete('/api/v1/metric/{}/'.format(metric_id))
        self.assertEqual(
            Metric.objects.count(),
            initial_metric_count - 1,
        )
        self.assertRaises(
            Metric.DoesNotExist,
            Metric.objects.get, id=metric_id,
        )

class ProductCreateTestCase(APITestCase):
    def test_create_product(self):
        initial_product_count = Product.objects.count()
        product_attrs = {
            'title': 'New Product',
            'description': 'Awesome product',
            'metrics': ["Metric 10","Metric 12"],
        }
        response = self.client.post('/api/v1/products/new', product_attrs)
        if response.status_code != 201:
            print(response.data)
        self.assertEqual(
            Product.objects.count(),
            initial_product_count + 1,
        )
        

class ProductDestroyTestCase(APITestCase):
    def test_delete_product(self):
        initial_product_count = Product.objects.count()
        product_id = Product.objects.get(title='New Product').id
        self.client.delete('/api/v1/products/{}/'.format(product_id))
        self.assertEqual(
            Product.objects.count(),
            initial_product_count - 1,
        )
        self.assertRaises(
            Product.DoesNotExist,
            Product.objects.get, id=product_id,
        )

class ProductListTestCase(APITestCase):
    def test_list_products(self):
        products_count = Product.objects.count()
        response = self.client.get('/api/v1/products/')
        self.assertIsNone(response.data['next'])
        self.assertIsNone(response.data['previous'])
        self.assertEqual(response.data['count'], products_count)
        self.assertEqual(len(response.data['results']), products_count)

class ProductUpdateTestCase(APITestCase):
    def test_update_product(self):
        product = Product.objects.get(title='New Product')
        response = self.client.patch(
            '/api/v1/products/{}/'.format(product.id),
            {
                'name': 'New Product',
                'description': 'Awesome product',
                'metrics': ["Metric 10"],
            },
            format='json',
        )
        updated = Product.objects.get(id=product.id)
        self.assertEqual(updated.name, 'New Product')