import json
import database
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
        db = database.Database()

        net_worth = 0
        price = 0

        user_id = int(self.request_handler.headers["authentication_key"].split('#', 1)[0])

        assets = db.getIndicators(user_id)

        for asset in assets:

            price = price + asset[2] * asset[3]
            net_worth = net_worth +  yf.Ticker(asset[1]).info["currentPrice"] * asset[2]

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
