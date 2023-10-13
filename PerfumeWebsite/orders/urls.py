from django.urls import path
from . import views






urlpatterns=[
    path('add_to_card',views.add_to_card,name='add_to_card'),
]