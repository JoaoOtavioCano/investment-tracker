class Authenticator:
    def __init__(self):
        self.authorization_list = {}

    def validateAuthentication(self, request):

        authentication_key = str(request.headers["Cookie"].split(";")[2].replace("authenticationKey=", "")).strip()

        user_id =str( authentication_key.split('#', 1)[0].strip())

        try:
            if self.authorization_list[user_id] == authentication_key:
                print("Entrou no True")
                return True
            else:
                return False
        except KeyError:
            return False 