from .database import Database
from .dolar import real_to_dolar

import json
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
        db = Database()

        user_id, _ = self.request_handler.authenticator.getUserIdAndAuthKeyFromCookies(self.request_handler)

        assets = db.getAssets(int(user_id))

        data = []


        for asset in assets:

            asset_type = asset[0]
            asset_name = str(asset[1])
            quantity = asset[2]
            
            print(yf.Ticker(asset_name).get_fast_info()["lastPrice"])

            if "stock(BR)" in asset_type:

                try:
                    avg_price = real_to_dolar(float(asset[3]))
                    current_price = real_to_dolar(float(yf.Ticker(asset_name).get_fast_info()["lastPrice"]))
                except:
                    current_price = avg_price = 1 
                asset_name = asset_name.replace(".SA", "")
            else:
                avg_price = asset[3]
                try:
                    current_price = yf.Ticker(asset_name).get_fast_info()["lastPrice"]
                    print(current_price)
                except:
                    current_price = avg_price
                    
            total = calculateTotal(quantity, current_price)
            gain_loss = calculateGainLoss(current_price, avg_price, quantity) 
            gain_loss_percent = calculateGainLossPercentage(current_price, avg_price)

            money_format = "${:.2f}"

            gain_loss = money_format.format(gain_loss)
            gain_loss_percent = "{:.2f}%".format(gain_loss_percent)
            total = money_format.format(total)
            avg_price = money_format.format(avg_price)

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
        
        print(data)

        return data
    

def calculateTotal(quantity, price_per_un):
    return quantity * price_per_un

def calculateGainLoss(current_price, avg_price, quantity):
    return (current_price - avg_price) * quantity 

def calculateGainLossPercentage(current_price, avg_price):
    return (current_price/avg_price - 1) * 100

def sortByTotal(e):
  return float(e['total'].replace("$", ''))
