from django.urls import path
from . import views


urlpatterns=[
    path('',views.products,name='products'),
    path('product/',views.product,name='product'),
    path('search/',views.search,name='search'),
]