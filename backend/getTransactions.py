import json
import database

class GetTransactions:

    def __init__(self, request_handler):
        self.request_handler =  request_handler

    def respond(self):

        response = self.__getDataFromDB__()

        json_response = json.dumps(response)

        self.request_handler.send_response(200, "OK")
        self.request_handler.send_header('Content-type', 'application/json')
        self.request_handler.end_headers()
        self.request_handler.wfile.write(json_response.encode('utf-8'))

    def __getDataFromDB__(self):
        db = database.Database()

        user_id = int(self.request_handler.headers["Cookie"].replace("authenticationKey=", "").split('#', 1)[0])

        transactions = db.getTransactions(user_id)

        data = []

        for transaction in transactions:

            date_time = formatDate(str(transaction[0]))
            asset_name = transaction[1]
            quantity = transaction[2]
            price = transaction[3]
            operation = transaction[4]
            total = calculateTotal(quantity, price)

            price = "${:.2f}".format(price)
            total = "${:.2f}".format(total)

            transaction_json = {
            "date_time": date_time,
            "asset": asset_name,
            "operation": operation,
            "quantity": quantity,
            "price": price,
            "total": total
            }
            
            data.append(transaction_json)

        return data
    
def calculateTotal(quantity, price_per_un):
    return quantity * price_per_un

def formatDate(date):
    year =  date.split()[0].split("-")[0]
    month =  date.split()[0].split("-")[1]
    day =  date.split()[0].split("-")[2]

    return f"{day}/{month}/{year}"