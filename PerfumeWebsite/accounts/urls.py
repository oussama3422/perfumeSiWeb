from django.urls import path
from . import views


urlpatterns=[
   path('sigin',views.signin,'sigin'),
   path('signup',views.signup,'signup')
]