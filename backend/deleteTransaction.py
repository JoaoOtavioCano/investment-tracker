import database

class DeleteTransaction:
    
    def __init__(self, request, payload):
        self.request = request
        self.payload = payload

    def respond(self):
        transaction_id = self.payload["transactionId"]

        self.__delete_transaction_from_db__(transaction_id)

        self.request.send_response(200, 'OK')
        self.request.end_headers()

    def __delete_transaction_from_db__(self, transaction_id):
        db = database.Database()

        db.delete_transaction(transaction_id)