from django.urls import path

from fireapp.views import api, LoginView, RegisterView, ChatView

urlpatterns = [
    path('', api, name='api'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('chat/', ChatView.as_view(), name='chat'),
]
