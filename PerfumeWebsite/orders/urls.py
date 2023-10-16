from django.urls import path
from . import views






urlpatterns=[
    path('add_to_cart',views.add_to_cart,name='add_to_cart'),
    path('cart',views.order,name='cart'),
    path('remove_from_cart/<int:orderdetails_id>',views.remove_from_card,name='remove_from_card'),
    path('add_qty<int:orderdetails_id>',views.add_quantity,name='add_qty'),
    path('minus_qty<int:orderdetails_id>',views.minus_quantity,name='minus_qty'),
    path('payment',views.payment,name='payment'),
]