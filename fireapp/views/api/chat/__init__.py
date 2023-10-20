from firebase_admin import firestore
from google.cloud.firestore_v1 import Query
from rest_framework import generics
from rest_framework.response import Response
from fireapp.serializers import ChatSerializer


class ChatView(generics.GenericAPIView):
    """
    get:
    Get all chat messages,
    Requires {Authorization: header}
    Optional {receiver_id: TextField, message: TextField}
    Success returns {chat: [{id: int, sender_id: int, receiver_id: int, message: str}, ...]}
    Failure returns {status: 401, code: 'Unauthorized', message: 'You don\'t have permission to access.', detail: 'Authentication credentials were not provided.', helper: 'Please include the {...,\'Authorization\': \'Bearer --ACCESS_TOKEN_HERE--\'} field in the request headers.'}

    post:
    Send a chat message,
    Requires {Authorization: header, receiver_id: int, message: str}
    Success returns {chat: [{id: int, sender_id: int, receiver_id: int, message: str}, ...]}
    Failure returns {status: 401, code: 'Unauthorized', message: 'You don\'t have permission to access.', detail: 'Authentication credentials were not provided.', helper: 'Please include the {...,\'Authorization\': \'Bearer --ACCESS_TOKEN_HERE--\'} field in the request headers.'}
    """

    serializer_class = ChatSerializer

    unauthorized_response = {
        'status': 401,
        'code': 'Unauthorized',
        'message': 'You don\'t have permission to access.',
        'detail': 'Authentication credentials were not provided.',
        'helper': 'Please include the {...,\'Authorization\': \'Bearer --ACCESS_TOKEN_HERE--\'} field in the request headers.'
    }

    def get(self, request):
        if not request.User:
            return Response(self.unauthorized_response, status=401)
        else:
            db = firestore.client()
            chat_ref = db.collection('chat')
            chat_docs = chat_ref.get()
            chat = [chat_doc.to_dict() for chat_doc in chat_docs]
            return Response(data={'chat': chat})

    def post(self, request):
        if not request.User:
            return Response(self.unauthorized_response, status=401)
        else:
            sender_id = int(request.User['id'])
            receiver_id = int(request.data['receiver_id'])
            message = request.data['message']

            db = firestore.client()
            chat_model = db.collection('chat')

            chat_count = chat_model.count().get()[0][0].value
            document_id = int(chat_count + 1)

            chat_model.document().set({
                'id': document_id,
                'sender_id': sender_id,
                'receiver_id': receiver_id,
                'message': message
            })

            chat_docs = chat_model.order_by('id', direction=Query.DESCENDING).get()
            chat = [chat_doc.to_dict() for chat_doc in chat_docs]
            return Response(data={'chat': chat})
