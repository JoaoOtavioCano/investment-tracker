class Logout:
    def __init__(self, request):
        self.request = request

        self.authenticator = request.authenticator

    def respond(self):
        user_id, _ = self.request.authenticator.getUserIdAndAuthKeyFromCookies(self.request)

        self.authenticator.authorization_list.pop(str(user_id))

        self.send_response(301, "OK")
        self.send_header('Location', 'https://investment-tracker.up.railway.app/login')
        self.end_headers()