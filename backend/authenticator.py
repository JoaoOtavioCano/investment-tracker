class Authenticator:
    def __init__(self):
        self.authorization_list = {}

    def validateAuthentication(self, request):

        user_id, authentication_key = self.getUserIdAndAuthKeyFromCookies(request)

        try:
            if self.authorization_list[user_id] == authentication_key:
                return True
            else:
                return False
        except KeyError:
            return False 
        
    def getUserIdAndAuthKeyFromCookies(self, request):
        cookies = request.headers["Cookie"].split(";")

        authentication_key = str([cookie for cookie in cookies if "authenticationKey=" in cookie][0]).replace("authenticationKey=", "").strip()

        user_id =str( authentication_key.split('#', 1)[0].strip())

        return user_id, authentication_key