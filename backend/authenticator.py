class Authenticator:
    def __init__(self):
        self.authorization_list = {}

    def validateAuthentication(self, request):

        authentication_key = request.headers["Cookie"].replace("authenticationKey=", "")

        user_id = authentication_key.split('#', 1)[0]

        try:
            if self.authorization_list[user_id] == authentication_key:
                return True
            else:
                return False
        except KeyError:
            return False 