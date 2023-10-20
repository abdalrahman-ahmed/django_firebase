from rest_framework import serializers
from fireapp.models import LoginModel


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        write_only=True,
        required=True,
        # help_text='Leave empty if no change needed',
        style={'input_type': 'email', 'placeholder': 'Email'}
    )

    password = serializers.CharField(
        write_only=True,
        required=True,
        # help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = LoginModel
        fields = ('email', 'password')