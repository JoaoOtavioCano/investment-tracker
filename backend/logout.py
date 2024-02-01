class Logout:
    def __init__(self, request):
        self.request = request

        self.authenticator = request.authenticator

    def respond(self):
        user_id, _ = self.request.authenticator.getUserIdAndAuthKeyFromCookies(self.request)

        self.authenticator.authorization_list.pop(str(user_id))

        self.request.send_response(200, "OK")
        self.request.end_headers()