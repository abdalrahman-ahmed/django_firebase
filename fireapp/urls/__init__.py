from django.urls import path, include


urlpatterns = [
    path('', include('fireapp.urls.home')),
    path('api/', include('fireapp.urls.api'), name='api'),
]
