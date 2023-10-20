from rest_framework import serializers
from fireapp.models import ChatModel


class ChatSerializer(serializers.ModelSerializer):
    receiver_id = serializers.EmailField(
        write_only=True,
        required=True,
        # help_text='Leave empty if no change needed',
        style={'input_type': 'text', 'placeholder': 'User ID'}
    )

    message = serializers.CharField(
        write_only=True,
        required=True,
        # help_text='Leave empty if no change needed',
        style={'input_type': 'text', 'placeholder': 'Message'}
    )

    authorization = serializers.CharField(
        min_length=1000,
        max_length=100000,
        write_only=True,
        required=True,
        help_text='This field is for testing purposes only through the \'Django REST Framework\'.',
        style={'input_type': 'text', 'placeholder': 'Ex: Bearer eyJhbGciO...'}
    )

    class Meta:
        model = ChatModel
        fields = ('receiver_id', 'message', 'authorization')