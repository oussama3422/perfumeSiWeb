from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth
from .models import UserProfile
import re
# Create your views here.


def signin(request):
    if request.method == 'POST' and 'signin_button' in request.POST:
        
        email=request.POST['email']
        password=request.POST['pass']
        user=auth.authenticate(email=email,password=password)
        if user is not None:
            auth.login(request,user)
            messages.success(request,'You are logged in successfully')
        else:
            pass



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
        messages.info(request,'This is Post Method')
        messages.success(request,'saved successfully')
        return redirect('profile')
    else:
        return render(request,'accounts/profile.html')