from .database import *
from .dolar import *

import json
import yfinance as yf

class GetIndicators():

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

        net_worth = 0
        price = 0

        user_id, _ = self.request_handler.authenticator.getUserIdAndAuthKeyFromCookies(self.request_handler)

        assets = db.getIndicators(int(user_id))

        for asset in assets:

            if "stock(BR)" in asset[0]:
                price = price + asset[2] * real_to_dolar(asset[3])
                net_worth = net_worth +  real_to_dolar(yf.Ticker(asset[1]).get_fast_info()["lastPrice"]) * asset[2]
            else:
                price = price + asset[2] * asset[3]
                net_worth = net_worth +  yf.Ticker(asset[1]).get_fast_info()["lastPrice"] * asset[2]

        gain_loss = net_worth - price

        net_worth = "${:.2f}".format(net_worth)
        price = "${:.2f}".format(price)
        gain_loss = "${:.2f}".format(gain_loss)

        data ={
            "net_worth": net_worth,
            "gain_loss": gain_loss,
            "price": price,
            }
            
        return data
