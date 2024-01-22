import database
import bcrypt

class NewPassword:
    def __init__(self, request, payload):
        self.request = request
        self.payload = payload

    def respond(self):
        code = self.payload["code"]
        new_password = self.payload["new_password"]

        user_id = self.__checkCode__(code)

        if user_id != -1:
            self.__chageUserPassword__(user_id, new_password)

            self.__deleteRequestToChangePassword__(user_id)

            self.request.send_response(200, "OK")
            self.request.end_headers()
        else:
            self.request.send_error(500, "INVALID CODE")
            self.request.end_headers()

    def __checkCode__(self, code):
        db = database.Database()

        user_id = db.getUserIdUsingCode(code)

        if user_id == None:
            return -1
        else:
            return user_id
        
    def __chageUserPassword__(self, user_id, new_password):
        salt = bcrypt.gensalt()

        new_password_hash = bcrypt.hashpw(new_password.encode(), salt).decode()
        
        db = database.Database()

        db.updateUserPassword(user_id, new_password_hash)

    def __deleteRequestToChangePassword__(self, user_id):
        db = database.Database()

        db.deletePasswordRequest(user_id)