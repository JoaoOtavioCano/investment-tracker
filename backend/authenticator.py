class Authenticator:
    def __init__(self):
        self.authorization_list = {}

    def validateAuthentication(self, request):

        authentication_key = request.headers["Cookie"].split(";")[2].replace("authenticationKey=", "")

        print(authentication_key)

        user_id = authentication_key.split('#', 1)[0]

        print(user_id)

        try:
            if self.authorization_list[user_id] == authentication_key:
                return True
            else:
                return False
        except KeyError:
            return False 