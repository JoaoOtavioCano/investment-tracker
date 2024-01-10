import json
import database
import random
import hashlib
import authCookie

class Login():

    def __init__(self, request_handler, payload):
        self.request_handler =  request_handler
        self.payload = payload
        
    def respond(self):

        user = self.__checkUserOnDB__()

        if user == False:
            self.request_handler.send_error(500, "USER NOT FOUND")
            self.request_handler.end_headers()
        else:

            authentication_key = __createAuthenticationKey__(user["userID"])

            user_id = authentication_key.split('#', 1)[0]

            self.request_handler.authenticator.authorization_list[user_id] = authentication_key

            cookie = authCookie.AuthCookie(authentication_key)

            response = {'user': user['user_name']}

            json_response = json.dumps(response)

            self.request_handler.send_response(200, "OK")
            self.request_handler.send_header('Set-Cookie', cookie.generateHTTPheaders())
            self.request_handler.send_header('Content-type', 'application/json')
            self.request_handler.end_headers()
            self.request_handler.wfile.write(json_response.encode('utf-8'))

    def __checkUserOnDB__(self):

        db = database.Database()

        email_hash =  hashlib.sha256(self.payload["email"].encode()).hexdigest()
        password_hash =  hashlib.sha256(self.payload["password"].encode()).hexdigest()

        user = db.getUser(email_hash, password_hash)

        if user == []:
            return False
        else:
            for info in user:
                data = {
                    "userID": info[0],
                    "user_name": info[1],
                }

            return data
         
def __createAuthenticationKey__(user_id):
    part01 = str(user_id).zfill(10)
    part02 = hashlib.sha256(str(random.randrange(9999999999)).encode()).hexdigest()
    return part01 + '#' + part02
    