from datetime import datetime, timezone
from firebase_admin import firestore, auth
from google.cloud.firestore_v1 import FieldFilter
from rest_framework import generics
from rest_framework.response import Response
from fireapp.serializers import RegisterSerializer


class RegisterView(generics.GenericAPIView):
    """
    get:
    Register a new user,
    Requires {name: TextField, email: EmailField, phone: TextField, password: TextField, confirm_password: TextField|match:password}

    post:
    Register a new user,
    Requires {name: str, email: str, phone: str, password: str, confirm_password: str|match:password}
    Success returns {success: True, user: {id: int, name: str, email: str, phone: str, created: date}, access_token: str}
    Failure returns {message: str}
    """

    serializer_class = RegisterSerializer

    default_message = 'This is the register api endpoint'
    user_exists_message = 'Register failed, User already exists'
    password_match_message = 'Register failed, Passwords do not match'

    def get(self, request):
        return Response(data={'message': self.default_message})

    def post(self, request):
        name = request.data['name']
        email = request.data['email']
        phone = request.data['phone']
        password = request.data['password']
        confirm_password = request.data['confirm_password']

        db = firestore.client()
        users_model = db.collection('users')
        users_docs = users_model.where(filter=FieldFilter('email', '==', email)).get()
        if len(users_docs) == 0:
            if password == confirm_password:
                users_count = users_model.count().get()[0][0].value
                document_id = int(users_count + 1)
                user = users_model.document(str(document_id))
                user.set({
                    'id': document_id,
                    'name': name,
                    'email': email,
                    'phone': phone,
                    'password': password,
                    'created': datetime.now(tz=timezone.utc),
                })
                user = user.get().to_dict()
                user.pop('password', None)
                token = auth.create_custom_token(str(user['id']))
                return Response(data={'success': True, 'user': user, 'access_token': token})
            else:
                return Response(data={'message': self.password_match_message})
        else:
            return Response(data={'message': self.user_exists_message})
