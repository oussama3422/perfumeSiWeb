from django.shortcuts import render,redirect
from django.contrib import messages
from products.models import Product
from orders.models import Order
from orders.models import OrderDetails
from django.utils import timezone
from .models import Payement



def  add_to_cart(request):
    if 'pro_id' in request.GET and 'Qty' in request.GET and 'price' in request.GET and request.user.is_authenticated and not request.user.is_anonymous:
        pro_id=request.GET['pro_id']
        qty=request.GET['Qty']

        order=Order.objects.all().filter(user=request.user,is_finished=False)
        # if not Product.objects.all().filter(id=pro_id).exists():
            # return redirect('products')
        pro=Product.objects.get(id=pro_id)
        if order:
            # old order
            old_order=Order.objects.get(user=request.user,is_finished=False)
            if OrderDetails.objects.filter(order=old_order,product=pro).exists():
                orderdetails = OrderDetails.objects.get(order=old_order,product=pro)
                orderdetails.quantity +=int(qty)
                orderdetails.save()
            else:
                orderdetails=OrderDetails.objects.create(product=pro,price=pro.price,quantity=qty,order=old_order)
            messages.success(request,'Was added to cart for old order')
        else:
            # new order
            new_order=Order()
            new_order.user = request.user
            new_order.is_finished=False
            new_order.order_date=timezone.now()
            new_order.save()
            orderdetails = OrderDetails.objects.create(product=pro,price=pro.price,quantity=qty,order=new_order)
            # messages.success(request,'Was added to cart for new order')
        return redirect('/products/'+request.GET['pro_id'])
    else:
        if 'pro_id' in request.GET:
            messages.error(request,'you must be logged in , if you want to add to cart.')
            return redirect('/products/'+request.GET['pro_id'])
        else:
            return redirect('index')


def order(request):
    
    context=None
    if request.user.is_authenticated and not request.user.is_anonymous:
        if Order.objects.all().filter(user=request.user,is_finished=False):
            order=Order.objects.get(user=request.user,is_finished=False)
            orderdetails=OrderDetails.objects.all().filter(order=order)
            total=0
            for sub in orderdetails:
                total +=sub.price * sub.quantity
            
            context={
                'order':order,
                'orderdetails':orderdetails,
                'total':total,
                }
     
    
    return render(request,'orders/cart.html',context)




def remove_from_card(request,orderdetails_id):
    if request.user.is_authenticated and not request.user.is_anonymous and orderdetails_id:
        orderdetails=OrderDetails.objects.get(id=orderdetails_id)
        orderdetails.delete()
        messages.success(request,'The item'+ orderdetails.product.name +'has been deleted Successfully')
    return redirect('cart')


# increase the quantity function

def add_quantity(request,orderdetails_id):
    if request.user.is_authenticated and not request.user.is_anonymous and orderdetails_id:
        orderdetails=OrderDetails.objects.get(id=orderdetails_id)
        if orderdetails.order.user.id == request.user.id:
            orderdetails.quantity +=1
            orderdetails.save()
    return redirect('cart')

# decrease the quantity function
def minus_quantity(request,orderdetails_id):
    if request.user.is_authenticated and not request.user.is_anonymous and orderdetails_id:
        orderdetails=OrderDetails.objects.get(id=orderdetails_id)
        if orderdetails.order.user.id == request.user.id:
            if orderdetails.quantity > 1:
                orderdetails.quantity -=1
                orderdetails.save()
    return redirect('cart')

# payment method

def payment(request):
    
    print(request.POST)
    context=None
    shipAddress=None
    shipPhone=None
    cardNumber=None
    Expiry=None
    securityCode=None
    is_added=None
    if request.method =='POST' and 'submitPayment' in request.POST and 'ship_address' in request.POST  and 'ship_phone' in request.POST and 'card_number' in request.POST and 'expiry' in request.POST and 'security_code' in request.POST:
        # after payment
        print('::::::::::::::::::::::::::::::::::>begin:::::>')
        shipAddress=request.POST['ship_address']
        print(shipAddress)
        shipPhone=request.POST['ship_phone']
        print(shipPhone)
        cardNumber=request.POST['card_number']
        print(cardNumber)
        Expiry=request.POST['expiry']
        print(Expiry)
        securityCode=request.POST['security_code']
        if request.user.is_authenticated and not request.user.is_anonymous:
            if Order.objects.all().filter(user=request.user,is_finished=False):
                order=Order.objects.get(user=request.user,is_finished=False)
                payment=Payement(order=order,shipment_address=shipAddress,shipment_phone=shipPhone,card_number=cardNumber,expiry=Expiry,security_code=securityCode,)
                payment.save()
                order.is_finished=True
                order.save()
                is_added=True
                messages.success(request,'Your order is done.')
        context={
            'ship_address':shipAddress,
            'ship_phone':shipPhone,
            'card_number':cardNumber,
            'expiry':Expiry,
            'security_code':securityCode,
            'is_added':is_added,
            }
        print(context)
    else:
        # before payment
        if request.user.is_authenticated and not request.user.is_anonymous:
            if Order.objects.all().filter(user=request.user,is_finished=False):
                order=Order.objects.get(user=request.user,is_finished=False)
                orderdetails=OrderDetails.objects.all().filter(order=order)
                total=0
                for sub in orderdetails:
                    total +=sub.price * sub.quantity
                context={
                'order':order,
                'orderdetails':orderdetails,
                'total':total,
                }
    print(context)
    return render(request,'orders/payment.html',context)



def show_orders(request):
    context=None
    if request.user.is_authenticated and not request.user.is_anonymous:
        all_orders = Order.objects.all().filter(user=request.user,is_finished=False)
        if all_orders:    
            order=Order.objects.get(user=request.user,is_finished=False)
            orderdetails=OrderDetails.objects.all().filter(order=order)
            total=0
            for sub in orderdetails:
                total +=sub.price * sub.quantity
            
            context={
                'order':order,
                'orderdetails':orderdetails,
                'total':total,
                }
    return render(request,'orders/show_orders.html',context)
    