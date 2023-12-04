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

        transactions = db.getTransactions(1)

        data = []

        for transaction in transactions:

            date_time = formatDate(str(transaction[0]))
            asset_name = transaction[1]
            quantity = transaction[2]
            price = transaction[3]
            total = calculateTotal(quantity, price)

            transaction_json = {
            "date_time": date_time,
            "asset": asset_name,
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
    hour_minute = date.split()[1][0] + date.split()[1][1] + ":" + date.split()[1][3] + date.split()[1][4]

    return day + "/" + month + "/" + year + " " + hour_minute