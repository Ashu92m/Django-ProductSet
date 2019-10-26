from django.db import models

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField(default='')
    metrics = models.ManyToManyField('Metric', blank=True, related_name='product_metrics')

    def __str__(self):
        return self.title

class Metric(models.Model):
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField(default='')

    def __str__(self):
        return self.title

class Issue(models.Model):

    issueTitle = models.CharField(max_length=200, unique=True)
    catagory = models.TextField(default='')
    product = models.ForeignKey(Product, related_name='+', null=True, on_delete=models.CASCADE)
    #product = models.ManyToManyField('Product', blank=True, related_name='product_issues')

    def __str__(self):
        return self.issueTitle
