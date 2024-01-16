import database
import bcrypt


class CreateAccount():
    def __init__(self, request, payload):
        self.request = request
        self.user_data = payload 

    def respond(self):
        self.__createUserOnDB__(self.user_data["name"],
                                self.user_data["email"],
                                self.user_data["password"])
        
        self.request.send_response(200, "Account created successfully")
        self.request.end_headers()

    def __createUserOnDB__(self, name, email, password):

        salt = bcrypt.gensalt()

        password_hash = bcrypt.hashpw(password.encode(), salt).decode()

        print(password_hash)

        db = database.Database()

        db.createUser(name, email, password_hash)



