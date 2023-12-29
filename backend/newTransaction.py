import database
import yfinance as yf

class newTransaction:
    def __init__(self, request, payload):
        self.request = request
        self.payload = payload

    def respond(self):

        if checkIfPayloadIsNotEmpty(self.payload):

            if checkStockExistance(self.payload["asset"]):
                self.__insertIntoDB__()
                self.__success_response__()
            else:
                self.__stock_does_not_exist_error_response__()
        else:
            self.__payload_with_empty_values_error_response__()

    def __insertIntoDB__(self):
        user_id = int(self.request.headers["authentication_key"].split('#', 1)[0])

        transaction = self.payload

        db = database.Database()

        db.addNewTransaction(user_id, 
                             asset=transaction["asset"], 
                             quantity=transaction["quantity"],
                             price=transaction["price"],
                             date=transaction["date"],
                             operation=transaction["operation"],
                             type=transaction["type"])
        
    def __success_response__(self):
        self.request.send_response(200, "OK")
        self.request.send_header('Content-type', 'plain/text')
        self.request.end_headers()
        
    def __stock_does_not_exist_error_response__(self):
        self.request.send_error(500, "Stock doesn't exist")
        self.request.send_header('Content-type', 'plain/text')
        self.request.end_headers()

    def __payload_with_empty_values_error_response__(self):
        self.request.send_error(500, "Empty values received by the server")
        self.request.send_header('Content-type', 'plain/text')
        self.request.end_headers()
        
def checkStockExistance(asset):
    try:
        yf.Ticker(asset).fast_info["lastPrice"]
        return True
    except KeyError:
        return False

def checkIfPayloadIsNotEmpty(payload):
    for key in payload:
        if payload[key] == "":
            return False
    return True 