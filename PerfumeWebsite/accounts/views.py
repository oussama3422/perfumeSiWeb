from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth
from .models import UserProfile
from products.models import Product
import re
# Create your views here.

def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect('index')
def signin(request):
    if request.method == 'POST' and 'signin_button' in request.POST:
        username=request.POST['fullname']
        password=request.POST['pass']
        user=auth.authenticate(username=username,password=password)
        print('user',user)
        if user is not None:
            if 'rememberme' not in request.POST:
                request.session.set_expiry(0)  # Session will expire when the user's browser is closed
            auth.login(request,user)
            messages.success(request,'You are logged in successfully')
        else:
            messages.error(request,'You Password or Email is not valid')
        return redirect('signin')
    else:    
        return render(request,'accounts/signin.html')
def signup(request):

    if request.method == 'POST' and 'signup_button' in request.POST:
        # variables for fields
        fullName=None
        phoneNum=None
        email=None
        password=None
        terms=None
        is_Added=None
        # get values from form
        if 'fullName' in request.POST : fullName=request.POST['fullName']
        else:messages.error(request,'Error in fullName ')

        if 'email' in request.POST : email=request.POST['email']
        else:messages.error(request,'Error in email ')

        if 'phoneNumber' in request.POST : phoneNum=request.POST['phoneNumber']
        else:messages.error(request,'Error in phoneNumber ')

        if 'password' in request.POST : password=request.POST['password']
        else:messages.error(request,'Error in password ')

        if 'terms' in request.POST : terms=request.POST['terms']

        # check the value
        if fullName and email and phoneNum and password:
            if terms=='on':
                # check if the username taken
                if User.objects.filter(username=fullName).exists():
                    print('Error found the user is already exists')
                    messages.error(request,'the user is already exists')
                else:
                    # check if the email is already exists
                    if User.objects.filter(email=email).exists():
                        print('Error found the email is already exists')
                        messages.error(request,'The email is already exists')
                    else:
                        patt="^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$"
                        if re.match(patt,email):
                            # add user
                            user = User.objects.create_user(username=fullName,email=email,password=password)
                            user.save()
                            # add user profile
                            userprofile=UserProfile(user=user,phoneNum=phoneNum)
                            userprofile.save()
                            #  clear fields
                            fullName=''
                            email=''
                            password=''
                            terms=None 
                            # access message
                            is_Added=True
                            messages.success(request,'the user has been created successfully ✅')
                        else:
                            messages.error(request,'Invalid Email')
            else:
                messages.error(request,'you must agree to the terms')
            
        else:
            messages.error(request,'check empty fields')
        context={'fullname':fullName,'email':email,'pass':password,'phone':phoneNum,'is_added':is_Added}
        return render(request,'accounts/signup.html',context)
    else:    
        return render(request,'accounts/signup.html')
    


def profile(request):
    if request.method == 'POST' and 'buttonchange' in request.POST:
        if request.user is not None and request.user.id !=None:
            userprofile=UserProfile.objects.get(user=request.user)
            if request.POST['fullname'] and request.POST['email'] and request.POST['password'] and request.POST['phoneNumber']:
                request.user.username=request.POST['fullname']
                userprofile.phoneNum=request.POST['phoneNumber']
                # request.user.email=request.POST['email']
                if not request.POST['password'].startswith('pbkdf2_sha256$'):
                    request.user.set_password(request.POST['password'])
                    request.user.save()
                    userprofile.save()
                    auth.login(request,request.user)
                    messages.success(request,'Your data has been saved successfully')
                else:
                    request.user.password = request.POST['password']
            else:
                messages.error(request,'Check your value and element.')
        return redirect('profile')
    else:
        if request.user is not None:
            context=None
            # if not request.user.id != None:
            if not request.user.is_anonymous:
                userprofile=UserProfile.objects.get(user=request.user)
                context={
                    'fullname':request.user.username,
                    'email':request.user.email,
                    'phonenumber':userprofile.phoneNum,
                    'password':request.user.password,
                }
            return render(request,'accounts/profile.html',context)
        else:
            return redirect('profile')



def favorite_product(request,pro_id):
    if request.user.is_authenticated and not request.user.is_anonymous:
        fav_prod = Product.objects.get(pk=pro_id)
        if UserProfile.objects.filter(user=request.user,product_favorites=fav_prod).exists():
            messages.warning(request,'Product has been Unfavorited')
        else:
            userprofile=UserProfile.objects.get(user=request.user)
            userprofile.product_favorites.add(fav_prod)
            messages.success(request,'Product has been favorited')
        return redirect('/products/' +str(pro_id))
    else:
            messages.error(request,'You must be logged in.')
        
    return redirect('index')


def show_products_favorite(request):
    context=None
    if request.user.is_authenticated and not request.user.is_anonymous:
        userInfo=UserProfile.objects.get(user=request.user)
        prod=userInfo.product_favorites.all()
        context={
            'products':prod,
        }
    return render(request,'products/products.html',context)