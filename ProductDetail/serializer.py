from rest_framework import serializers

from .models import Product, Metric, Issue

class MetricSerializer(serializers.ModelSerializer):

    related = serializers.SerializerMethodField()

    class Meta:
        model = Metric
        fields = ( 'id', 'title', 'description', 'related')

    def get_related(self, obj):
        Value = {'products':None, 'issues':None}
        try:
            Value['products'] = obj.product_metrics.values_list('title', flat=True)
            try:
                issue = Issue.objects.filter(product__title__in=Value['products'])
                Value['issues'] = issue.values_list('issueTitle', flat=True)
            except:
                pass
        except:
            pass

        return Value

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    def create(self, validated_data):
        return Metric.objects.create(**validated_data)

class MetricProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Metric
        fields = ( 'title', 'description')

class ProductSerializer(serializers.ModelSerializer):

    metrics = MetricProductSerializer( many=True)
    issues = serializers.SerializerMethodField()

    
    class Meta:
        model = Product
        fields = ( 'id', 'title', 'description', 'metrics', 'issues')

    def get_issues(self, instance):
        try:
            issue = Issue.objects.filter(product=instance)
            Value = issue.values_list('issueTitle', flat=True)
        except Issue.DoesNotExist:
            Value = None
        return Value
        #return IssueProductSerializer(issue).data

class IssueSerializer(serializers.ModelSerializer):

    product = serializers.CharField(source='product.title', default=None)
    metrics = serializers.SerializerMethodField('get_metrics')
    #serializers.CharField(source='product.metrics')

    class Meta:
        model = Issue
        fields = ( 'id', 'issueTitle', 'catagory', 'product', 'metrics')

    def get_metrics(self, obj):
        if obj.product == None:
            return None
        return obj.product.metrics.values_list('title', flat=True)

    def create(self, validated_data):
        #id_data=validated_data.pop('product')
        
        try:
            Values = Product.objects.get(title=validated_data['product']['title'])
        except Product.DoesNotExist:
            raise ValidationError({ 'Product': 'The Product Title sent is incorrect (No such Product exists)' })

        issue = Issue.objects.create (issueTitle=validated_data['issueTitle'],
        catagory=validated_data['catagory'])
        issue.save()
        
        issue.product=Values
        
        issue.save()
        
        return issue

        #return Issue.objects.create(**validated_data)

    def update(self, instance, validated_data):
        
        Values = Product.objects.get(title=validated_data.pop('product')['title'])
        instance.product=Values
        
        instance.save()
        
        return super().update(instance, validated_data)





