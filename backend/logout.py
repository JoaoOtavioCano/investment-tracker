class Logout:
    def __init__(self, request):
        self.request = request

        self.authenticator = request.authenticator

    def respond(self):
        user_id, _ = self.request.authenticator.getUserIdAndAuthKeyFromCookies(self.request)

        self.authenticator.authorization_list.pop(str(user_id))

        self.request.send_response(302, "OK")
        self.request.send_header('Location', 'https://investment-tracker.up.railway.app/login')
        self.request.end_headers()