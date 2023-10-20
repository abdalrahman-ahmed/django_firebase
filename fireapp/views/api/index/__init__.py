from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def api(request):
    """
    Return a list of all the existing api endpoints.
    """
    secure = request.is_secure()
    host = request.META.get('HTTP_HOST')
    origin = f'http{secure and "s" or ""}://{host}'
    routes = [
        f'{origin}/api/register/',
        f'{origin}/api/login/',
        f'{origin}/api/chat/',
    ]

    return Response(routes)
