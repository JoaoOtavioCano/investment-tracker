class Authenticator:
    def __init__(self):
        self.authorization_list = {}

    def validateAuthentication(self, request):

        authentication_key = request.headers["Cookie"].split(";")[2].replace("authenticationKey=", "")

        print(authentication_key)

        user_id = authentication_key.split('#', 1)[0].strip()

        print(user_id)
        print(self.authorization_list)
        print(self.authorization_list[str(user_id)])

        try:
            if self.authorization_list[user_id] == authentication_key:
                print("Entrou no True")
                return True
            else:
                return False
        except KeyError:
            return False 