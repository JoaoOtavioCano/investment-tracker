import database
import yfinance as yf
import possibleErrors
from payloadValidator import PayloadValidator

class newTransaction:
    def __init__(self, request, payload):
        self.request = request
        self.payload = payload

    def respond(self):
        expected_payload_keys = ["asset", "quantity", "price", "date", "operation", "type"]

        payload_validator = PayloadValidator()
        
        if not payload_validator.validate(self.payload, expected_payload_keys):
            self.__invalid_payload__()
        else:
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

    def __insertIntoDB__(self):
        user_id, _ = self.request.authenticator.getUserIdAndAuthKeyFromCookies(self.request)
        

        transaction = self.payload

        db = database.Database()

        try:
            db.addNewTransaction(int(user_id), 
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

    def __invalid_payload__(self):
        self.request.send_error(500, "INVALID PAYLOAD")
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
        if yf.Ticker(asset).fast_info["lastPrice"] != None:
            return True
        else:
            return False
    except KeyError:
        return False, 0