from django.shortcuts import get_object_or_404,render
from .models import Product
# Create your views here.


def products(request):
    pro=Product.objects.all()
    name=None
    desc=None
    min_price=None
    max_price=None
    checkbox=None
    if 'checkbox' in request.GET:
        checkbox=request.GET.get('checkbox')
        if not checkbox:
            checkbox='off'
    # filter by name
    if 'q' in request.GET:
        name=request.GET['q']
        if name:
            if checkbox =='on':
                pro=pro.filter(name__contains=name)
            else:
                pro=pro.filter(name__icontains=name)
    # filter by description
    if 'desc' in request.GET:
        desc=request.GET['desc']
        if desc:
            if checkbox =='on':
                pro=pro.filter(desc__contains=desc)
            else:
                pro=pro.filter(desc__icontains=desc)
    
    # filter by price
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    # Check if min_price and max_price are valid integers
    if min_price and max_price:
        if min_price.isdigit() and max_price.isdigit():
            min_price = int(min_price)
            max_price = int(max_price)
            # Now, filter the queryset
            pro = pro.filter(price__gte=min_price, price__lte=max_price)

    context={
        'products':pro,
    }
    return render(request,'products/products.html',context)

def product(request,prod_id):
    context={
        'pro':get_object_or_404(Product,pk=prod_id)
    }
    return render(request,'products/product.html',context)

def search(request):
    return render(request,'products/search.html')
