import http.cookies as cookies

class AuthCookie():
    def __init__(self, authentication_key):
        self.cookie = cookies.SimpleCookie()

        self.cookie["authenticationKey"] = authentication_key

        self.cookie["authenticationKey"]["httponly"] = True 
    
    def generateHTTPheaders(self):
        return str(self.cookie).replace("Set-Cookie: ", "")