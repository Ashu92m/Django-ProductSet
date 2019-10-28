from django.test import TestCase

# Create your tests here.
import os.path
from django.conf import settings

from rest_framework.test import APITestCase

from ProductDetail.models import Product, Metric, Issue


class MetricTestCase(APITestCase):

    def setUp(self):
        Metric.objects.create(title="Metric 10", description="Metric Number 10")
        Metric.objects.create(title="Metric 12", description="Metric Number 11")

    def test_create_metric(self):
        initial_product_count = Metric.objects.count()
        metric_attrs = {
            'title': 'Metric 13',
            'description': 'Metric Number 13',
        }
        response = self.client.post('/api/v1/metric/add', metric_attrs)
        if response.status_code != 201:
            print(response.status_code)

        self.assertEqual(
            Metric.objects.count(),
            initial_product_count + 1,
        )

    def test_update_metric(self):
        metric_id = Metric.objects.get(title='Metric 12').id
        response = self.client.patch(
            '/api/v1/metric/{}/'.format(metric_id),
            {
                'title': 'Metric 12',
                'description': 'Metric Number 12',
            },
            format='json',
        )
        updated = Metric.objects.get(id=metric_id)
        self.assertEqual(updated.description, 'Metric Number 12')

    def test_delete_metric(self):
        initial_metric_count = Metric.objects.count()
        metric_id = Metric.objects.get(title='Metric 10').id
        self.client.delete('/api/v1/metric/{}/'.format(metric_id))
        self.assertEqual(
            Metric.objects.count(),
            initial_metric_count - 1,
        )
        self.assertRaises(
            Metric.DoesNotExist,
            Metric.objects.get, id=metric_id,
        )



class ProductTestCase(APITestCase):

    def setUp(self):
        metric1 = Metric.objects.create(title="Metric 10", description="Metric Number 10")
        metric2 = Metric.objects.create(title="Metric 12", description="Metric Number 12")
        metric3 = Metric.objects.create(title="Metric 13", description="Metric Number 13")
        product1 = Product.objects.create(title="Product 1", description="Product Number 1")
        product1.metrics.set([metric1,metric2])
        product2= Product.objects.create(title="Product 2", description="Product Number 11")
        product2.metrics.set([metric3,metric2])

    def test_create_product(self):
        initial_product_count = Product.objects.count()
        product_attrs = {
            "title": "Product 3",
            "description": "Product Number 3",
            "metrics": ["Metric 10", "Metric 12"],
        }
        response = self.client.post('/api/v1/product/add', product_attrs, format='json')
        if response.status_code != 201:
            print(response.data)

        self.assertEqual(
            Product.objects.count(),
            initial_product_count + 1,
        )

    def test_update_product(self):
        product_id = Product.objects.get(title='Product 2').id
        product_attrs = {
            "title": "Product 2",
            "description": "Product Number 2",
            "metrics": ["Metric 10"],
        }
        
        response = self.client.put('/api/v1/product/{}/'.format(product_id), product_attrs)

        if response.status_code != 201:
            print(response.data)
        updated = Product.objects.get(id=product_id)
        self.assertEqual(updated.metrics.values('title'), 'Metric 10')

    def test_delete_product(self):
        initial_product_count = Product.objects.count()
        product_id = Product.objects.get(title='Product 2').id
        self.client.delete('/api/v1/product/{}/'.format(product_id))
        self.assertEqual(
            Product.objects.count(),
            initial_product_count - 1,
        )
        self.assertRaises(
            Product.DoesNotExist,
            Product.objects.get, id=product_id,
        )


    