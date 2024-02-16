import database
import bcrypt
from payloadValidator import PayloadValidator
import possibleErrors

class CreateAccount():
    def __init__(self, request, payload):
        self.request = request
        self.user_data = payload 

    def respond(self):
        expected_payload_keys = ["name", "email", "password"]

        payload_validator = PayloadValidator()
        
        if not payload_validator.validate(self.user_data, expected_payload_keys):
            self.request.send_error(500, "INVALID PAYLOAD")
            self.request.end_headers()
        else:
            try:
                self.__createUserOnDB__(self.user_data["name"],
                                        self.user_data["email"],
                                        self.user_data["password"])
                
                self.request.send_response(200, "Account created successfully")
                self.request.end_headers()
            except possibleErrors.UserAlreadyExists:
                self.request.send_response(500, "Email already exists")
                self.request.end_headers()
                self.request.wfile.write(b"Email already exists")

    def __createUserOnDB__(self, name, email, password):

        salt = bcrypt.gensalt()

        password_hash = bcrypt.hashpw(password.encode(), salt).decode()

        db = database.Database()

        try:
            db.createUser(name, email, password_hash)
        except possibleErrors.UserAlreadyExists:
            raise possibleErrors.UserAlreadyExists


