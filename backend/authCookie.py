import http.cookies as cookies

class AuthCookie():
    def __init__(self, authentication_key):

        hours = 3600

        self.cookie = cookies.SimpleCookie()

        self.cookie["authenticationKey"] = authentication_key

        self.cookie["authenticationKey"]["httponly"] = True 
        self.cookie["authenticationKey"]["samesite"] = 'Lax' 
        self.cookie["authenticationKey"]["max-age"] =  2 * hours
    
    def generateHTTPheaders(self):
        return str(self.cookie).replace("Set-Cookie: ", "")