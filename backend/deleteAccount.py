from .database import Database

class DeleteAccount():
    def __init__(self, request):
        self.request = request

        self.authenticator = request.authenticator

    def respond(self):
        user_id, _ = self.request.authenticator.getUserIdAndAuthKeyFromCookies(self.request)

        self.__delete_from_db___(user_id)

        self.request.send_response(200, "OK")
        self.request.end_headers()

    def __delete_from_db___(self, user_id):
        db = Database()

        db.deleteUser(user_id)