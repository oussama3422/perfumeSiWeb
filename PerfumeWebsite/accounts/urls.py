from django.urls import path
from . import views

urlpatterns = [
    path('signin', views.signin, name='signin'),  # Use a trailing slash for consistency
    path('signup', views.signup, name='signup'),  # Use a trailing slash for consistency
    path('profile', views.profile, name='profile'),  # Use a trailing slash for consistency
    path('logout', views.logout, name='logout'),  # Use a trailing slash for consistency
]
