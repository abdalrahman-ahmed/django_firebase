from rest_framework import generics
from rest_framework.response import Response
from firebase_admin import firestore, auth
from google.cloud.firestore_v1 import FieldFilter
from fireapp.serializers import LoginSerializer


class LoginView(generics.GenericAPIView):
    """
    get:
    Login a user,
    Requires {email: EmailField, password: TextField}

    post:
    Login a user,
    Requires {email: str, password: str}
    Success returns {message: str, user: {id: int, name: str, email: str, phone: str, created: date}, access_token: str}
    Failure returns {message: str}
    """

    serializer_class = LoginSerializer

    default_message = 'This is the login api endpoint'
    failure_message = 'Login failed, incorrect email or password please try again.'

    def get(self, request):
        return Response(data={'message': self.default_message})

    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        db = firestore.client()
        users_model = db.collection('users')
        user = users_model.where(filter=FieldFilter('email', '==', email)).where(filter=FieldFilter('password', '==', password)).get()

        if len(user) > 0:
            user = user[0].to_dict()
            user.pop('password', None)
            token = auth.create_custom_token(str(user['id']))
            return Response(data={'success': True, 'user': user, 'access_token': token})
        else:
            return Response(data={'message': self.failure_message})
