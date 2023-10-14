from django.urls import path
from . import views






urlpatterns=[
    path('add_to_cart',views.add_to_cart,name='add_to_cart'),
    path('cart',views.order,name='cart'),
    path('<int:orderdetails_id>',views.remove_from_card,name='remove_from_card'),
]