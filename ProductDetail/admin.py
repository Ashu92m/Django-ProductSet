from django.contrib import admin
from .models import Product,Metric,Issue
# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'description']

@admin.register(Metric)
class MetricAdmin(admin.ModelAdmin):
    list_display = ['title', 'description']

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ['issueTitle', 'catagory']
