from django.shortcuts import render,redirect
from django.contrib import messages
from products.models import Product
from orders.models import Order
from orders.models import OrderDetails
from django.utils import timezone




def  add_to_cart(request):
    if 'pro_id' in request.GET and 'Qty' in request.GET and 'price' in request.GET and request.user.is_authenticated and not request.user.is_anonymous:
        pro_id=request.GET['pro_id']
        qty=request.GET['Qty']

        order=Order.objects.all().filter(user=request.user,is_finished=False)
        if order:
            # new order
            messages.success(request,'there  is old product')
        else:
            # odd order
            messages.success(request,'you did new order')
            pass
        return redirect('/products/'+request.GET['pro_id'])
    else:
        return redirect('products')


