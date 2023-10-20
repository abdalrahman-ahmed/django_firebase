from rest_framework import serializers
from fireapp.models import RegisterModel


class RegisterSerializer(serializers.ModelSerializer):
    name = serializers.EmailField(
        write_only=True,
        required=True,
        # help_text='Leave empty if no change needed',
        style={'input_type': 'text', 'placeholder': 'Name'}
    )

    email = serializers.EmailField(
        write_only=True,
        required=True,
        # help_text='Leave empty if no change needed',
        style={'input_type': 'email', 'placeholder': 'Email'}
    )

    phone = serializers.EmailField(
        write_only=True,
        required=True,
        # help_text='Leave empty if no change needed',
        style={'input_type': 'text', 'placeholder': 'Phone'}
    )

    password = serializers.CharField(
        write_only=True,
        required=True,
        # help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    confirm_password = serializers.CharField(
        write_only=True,
        required=True,
        # help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Confirm Password'}
    )

    class Meta:
        model = RegisterModel
        fields = ('name', 'email', 'phone', 'password', 'confirm_password')
