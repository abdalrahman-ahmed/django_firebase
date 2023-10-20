from django.urls import path
from fireapp.views import home

urlpatterns = [
    path('', home, name='index'),
]
