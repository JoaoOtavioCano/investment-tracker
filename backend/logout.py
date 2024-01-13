class Logout:
    def __init__(self, request):
        self.request = request

        self.authenticator = request.authenticator

    def respond(self):
        user_id = self.request.headers["Cookie"].replace("authenticationKey=", "").split('#', 1)[0]

        self.authenticator.authorization_list.pop(user_id)

        self.request.send_response(200, "OK")
        self.request.end_headers()