from .database import *
from .payloadValidator import PayloadValidator

class DeleteTransaction:
    
    def __init__(self, request, payload):
        self.request = request
        self.payload = payload

    def respond(self):
        expected_payload_keys = ["transactionId"]

        payload_validator = PayloadValidator()
        
        if not payload_validator.validate(self.payload, expected_payload_keys):
            self.request.send_error(500, "INVALID PAYLOAD")
            self.request.end_headers()

        else:
            transaction_id = self.payload["transactionId"]

            self.__delete_transaction_from_db__(transaction_id)

            self.request.send_response(200, 'OK')
            self.request.end_headers()

    def __delete_transaction_from_db__(self, transaction_id):
        db = Database()

        db.delete_transaction(transaction_id)