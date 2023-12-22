import json
import database
import yfinance as yf

class GetAssets:

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

        user_id = int(self.request_handler.headers["authentication_key"].split('#', 1)[0])

        assets = db.getAssets(user_id)

        data = []


        for asset in assets:

            asset_type = asset[0]
            asset_name = asset[1]
            quantity = asset[2]
            avg_price = asset[3]
            current_price = yf.Ticker(asset_name).fast_info["lastPrice"]
            total = calculateTotal(quantity, current_price)
            gain_loss = calculateGainLoss(current_price, avg_price, quantity) 
            gain_loss_percent = calculateGainLossPercentage(current_price, avg_price)

            gain_loss = "${:.2f}".format(gain_loss)
            gain_loss_percent = "{:.2f}%".format(gain_loss_percent)
            total = "${:.2f}".format(total)

            asset_json = {
            "type": asset_type,
            "asset": asset_name,
            "quantity": quantity,
            "avg_price": avg_price,
            "gain_loss": gain_loss,
            "gain_loss_percent": gain_loss_percent,
            "total": total,
            }
            
            data.append(asset_json)

        data.sort(key=sortByTotal, reverse=True)

        return data
    

def calculateTotal(quantity, price_per_un):
    return quantity * price_per_un

def calculateGainLoss(current_price, avg_price, quantity):
    return (current_price - avg_price) * quantity 

def calculateGainLossPercentage(current_price, avg_price):
    return (current_price/avg_price - 1) * 100

def sortByTotal(e):
  return float(e['total'].replace("$", ''))
