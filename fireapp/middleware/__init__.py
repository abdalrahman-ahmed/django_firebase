from django.utils.deprecation import MiddlewareMixin
from firebase_admin import firestore, auth
from django.conf import settings


class FirebaseAuthenticationMiddleware(MiddlewareMixin):
    User = firestore.client().collection('users')

    def process_request(self, request):
        request.User = None
        authorization_header = str(request.META.get('HTTP_AUTHORIZATION'))
        if settings.DEBUG and not authorization_header.startswith('Bearer '):
            authorization_header = request.method == 'POST' and request.POST.get('authorization') or ""
        if authorization_header and authorization_header.startswith('Bearer '):
            token = authorization_header.split(' ')
            if len(token) > 1:
                id_token = token[1]
                jwd = auth.verify_id_token(id_token)
                document_id = jwd['uid']
                user = self.User.document(document_id).get()
                if user.exists:
                    request.User = user.to_dict()
