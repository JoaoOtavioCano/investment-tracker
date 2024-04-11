import yfinance as yf

def real_to_dolar(amount):
    convertion = yf.Ticker("BRLUSD=X").fast_info["lastPrice"]
    return amount * convertion 

if __name__ == '__main__':
    print(yf.Ticker("WEGE3.SA").fast_info["lastPrice"])
