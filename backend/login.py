import json
import database
import random

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
            authentication_key = __createAuthenticationKey__()

            authentication_register = {
                'authentication_key': authentication_key,
                'IP_address': self.request_handler.client_address[0],
                'user_id': user[0]["userID"]
            }

            self.request_handler.authorization_list.append(authentication_register)

            authentication_json = {
                'authorized': 'true',
                'authenticationKey': authentication_key
            }

            json_response = json.dumps(authentication_json)

            self.request_handler.send_response(200, "OK")
            self.request_handler.send_header('Content-type', 'application/json')
            self.request_handler.end_headers()
            self.request_handler.wfile.write(json_response.encode('utf-8'))

    def __checkUserOnDB__(self):

        db = database.Database()

        user = db.getUser(self.payload["email"], self.payload["password"])

        if user == []:
            return False
        else:
            for info in user:
                data = [{
                    "userID": info[0],
                }]

            return data
         
def __createAuthenticationKey__():
    return random.randrange(9999999999)