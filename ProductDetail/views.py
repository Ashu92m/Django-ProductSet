from django.shortcuts import render
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, CreateAPIView, \
    RetrieveUpdateDestroyAPIView, GenericAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework import status
from .serializer import ProductSerializer, MetricSerializer, IssueSerializer
from .models import Product, Metric, Issue
# Create your views here.

class ProductsPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100

class ProductList(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ('id',)
    search_fields = ('title', 'description')
    #pagination_class = ProductsPagination


class ProductCreate(CreateAPIView):
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):

        #return super().create(request, *args, **kwargs)

        try:
            title = request.data.get('title')
            if len(title)>200:    
                raise ValidationError({ 'title': 'A tilte/Name is required' })
        except ValueError:
            raise ValidationError({ 'title': 'A tilte/Name is required' })

        Values = ''

        if request.data.get('metrics') != None:
            Query = request.data.get('metrics')
            if type(Query) == type(''):
                Query = Query.split(',')
            for i in Query:
                try:
                    Value = Metric.objects.get(title=i)
                except:
                    raise ValidationError({ 'Metrics': i + ' Metric Not found' })
                
            Values = Metric.objects.filter(title__in=Query)
        product = Product.objects.create (title=request.data.get('title'), description=request.data.get('description') )
        product.metrics.set(Values)
        
        product.save()
        
        if Product.objects.get(title=request.data.get('title')) != None:
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
        
        
class ProductRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    lookup_field = 'id'
    serializer_class = ProductSerializer

    def delete(self, request, *args, **kwargs):
        product_id = request.data.get('id')
        response = super().delete(request, *args, **kwargs)
        if response.status_code == 204:
            from django.core.cache import cache
            cache.delete('product_data_{}'.format(product_id))
        return response

    def update(self, request, *args, **kwargs):
        instance = Product.objects.get(title=request.data.get('title'))
        if request.data.get('metrics') == None:
            instance.metrics.set('')
        else:
            Query = request.data.get('metrics')
            if type(Query) == type(''):
                Query = Query.split(',')

            Values = Metric.objects.filter(title__in=Query)
            if not list(Values):
                return Response({"Metric": ', '.join(Query) + " Not found"}, status=status.HTTP_400_BAD_REQUEST)
            instance.metrics.set(Values)

        instance.title = request.data.get('title')
        instance.description = request.data.get('description')

        instance.save()
    
        return Response(status=status.HTTP_200_OK)


class MetricList(ListAPIView):
    queryset = Metric.objects.all()
    serializer_class = MetricSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ('id',)
    search_fields = ('title', 'description')
    #pagination_class = ProductsPagination


class MetricCreate(CreateAPIView):
    serializer_class = MetricSerializer

    def create(self, request, *args, **kwargs):
        try:
            title = request.data.get('title')
            if len(title)>200:    
                raise ValidationError({ 'price': 'Must be above $0.00' })
        except ValueError:
            raise ValidationError({ 'title': 'A tilte/Name is required' })
        return super().create(request, *args, **kwargs)

class MetricRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = Metric.objects.all()
    lookup_field = 'id'
    serializer_class = MetricSerializer

    def delete(self, request, *args, **kwargs):
        metric_id = request.data.get('id')
        response = super().delete(request, *args, **kwargs)
        if response.status_code == 204:
            from django.core.cache import cache
            cache.delete('metric_data_{}'.format(metric_id))
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        if response.status_code == 200:
            from django.core.cache import cache
            metric = response.data
            cache.set('metric_data_{}'.format(metric['id']), {
                'title': metric['title'],
                'description': metric['description'],
            })
        return response


class IssueList(ListAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ('id',)
    search_fields = ('issueTitle', 'catagory')
    #pagination_class = ProductsPagination


class IssueCreate(CreateAPIView):
    serializer_class = IssueSerializer

    def create(self, request, *args, **kwargs):
        try:
            title = request.data.get('issueTitle')
            if len(title)>200:    
                raise ValidationError({ 'price': 'Must be above $0.00' })
        except ValueError:
            raise ValidationError({ 'title': 'A tilte/Name is required' })

        return super().create(request, *args, **kwargs)

class IssueRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = Issue.objects.all()
    lookup_field = 'id'
    serializer_class = IssueSerializer

    def delete(self, request, *args, **kwargs):
        issue_id = request.data.get('id')
        response = super().delete(request, *args, **kwargs)
        if response.status_code == 204:
            from django.core.cache import cache
            cache.delete('issue_data_{}'.format(issue_id))
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        if response.status_code == 200:
            from django.core.cache import cache
            issue = response.data
            cache.set('issue_data_{}'.format(issue['id']), {
                'issueTitle': issue['issueTitle'],
                'catagory': issue['catagory'],
                'products': issue['product'],
            })
        return response
