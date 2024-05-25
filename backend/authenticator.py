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
        """"
        try:
            cookies = request.headers["Cookie"].split(";")
            authentication_key = str([cookie for cookie in cookies if "authenticationKey=" in cookie][0]).replace("authenticationKey=", "").strip()
        except (IndexError, AttributeError):
            raise AuthCookieNotFound
        """
        authentication_key = "foda-se"
        user_id = "00004"

        return user_id, authentication_key