"""ProductInfo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

import ProductDetail.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('product/', ProductDetail.views.ProductList.as_view()),
    path('product/add', ProductDetail.views.ProductCreate.as_view()),
    path('product/<int:id>/', ProductDetail.views.ProductRetrieveUpdateDestroy.as_view()),
    path('metric/', ProductDetail.views. MetricList.as_view()),
    path('metric/add', ProductDetail.views. MetricCreate.as_view()),
    path('metric/<int:id>/', ProductDetail.views.MetricRetrieveUpdateDestroy.as_view()),
    path('issue/', ProductDetail.views.IssueList.as_view()),
    path('issue/add', ProductDetail.views.IssueCreate.as_view()),
    path('issue/<int:id>/', ProductDetail.views.IssueRetrieveUpdateDestroy.as_view())
]
