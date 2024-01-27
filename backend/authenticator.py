class Authenticator:
    def __init__(self):
        self.authorization_list = {}

    def validateAuthentication(self, request):
        print(request.headers["Cookie"])
        print(request.headers["Cookie"][2])

        authentication_key = request.headers["Cookie"][2].replace("authenticationKey=", "")

        user_id = authentication_key.split('#', 1)[0]

        try:
            if self.authorization_list[user_id] == authentication_key:
                return True
            else:
                return False
        except KeyError:
            return False 