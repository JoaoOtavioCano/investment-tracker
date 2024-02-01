from possibleErrors import AuthCookieNotFound

class Authenticator:
    def __init__(self):
        self.authorization_list = {}

    def validateAuthentication(self, request):

        try:
            user_id, authentication_key = self.getUserIdAndAuthKeyFromCookies(request)
        except AuthCookieNotFound:
            return False

        try:
            if self.authorization_list[user_id] == authentication_key:
                return True
            else:
                return False
        except KeyError:
            return False 
        
    def getUserIdAndAuthKeyFromCookies(self, request):
        cookies = request.headers["Cookie"].split(";")

        try:
            authentication_key = str([cookie for cookie in cookies if "authenticationKey=" in cookie][0]).replace("authenticationKey=", "").strip()
        except IndexError:
            raise AuthCookieNotFound

        user_id =str( authentication_key.split('#', 1)[0].strip())

        return user_id, authentication_key