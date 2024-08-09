from django.contrib.auth import login, authenticate


class AutoLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        username = request.session.get('username')
        password = request.session.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

        response = self.get_response(request)

        return response
