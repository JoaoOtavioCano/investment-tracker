import database
import yfinance as yf
import possibleErrors

class newTransaction:
    def __init__(self, request, payload):
        self.request = request
        self.payload = payload

    def respond(self):

        if checkIfPayloadIsNotEmpty(self.payload):

            if checkStockExistance(self.payload["asset"]):
                try:
                    self.__insertIntoDB__()
                    self.__success_response__()
                except possibleErrors.AssetNotInPortfolio:
                    self.__asset_not_in_portfolio_error_response__()
                except possibleErrors.NegativeQuantity:
                    self.__negative_quantity_error_response__()
            else:
                self.__stock_does_not_exist_error_response__()
        else:
            self.__payload_with_empty_values_error_response__()

    def __insertIntoDB__(self):
        user_id = int(self.request.headers["Cookie"].replace("authenticationKey=", "").split('#', 1)[0])

        transaction = self.payload

        db = database.Database()

        try:
            db.addNewTransaction(user_id, 
                                asset=transaction["asset"], 
                                quantity=transaction["quantity"],
                                price=transaction["price"],
                                date=transaction["date"],
                                operation=transaction["operation"],
                                type=transaction["type"])
        
        except possibleErrors.AssetNotInPortfolio:
            raise possibleErrors.AssetNotInPortfolio
        except possibleErrors.NegativeQuantity:
            raise possibleErrors.NegativeQuantity
        
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
    
    def __negative_quantity_error_response__(self):
        self.request.send_error(500, "Impossible sell more than it is possessed")
        self.request.send_header('Content-type', 'plain/text')
        self.request.end_headers()
        
    def __asset_not_in_portfolio_error_response__(self):
        self.request.send_error(500, "Asset doesn't exist in the portfolio")
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