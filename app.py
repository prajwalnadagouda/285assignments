from flask import Flask, request
import yfinance as yf
from datetime import datetime, timezone
from requests.exceptions import ConnectionError
import pytz

app = Flask(__name__)

@app.route('/')
def hello_world():
    StockSymbol = request.args.get('stock') 
    try:
        # StockSymbol =input("Please enter a symbol:\n")
        stock = yf.Ticker(StockSymbol)
        info = stock.info
        companyName = info['longName']
        stockPrice = float(info['currentPrice'])
        previousPrice= float(info['previousClose'])
        # print(stock_price,previous_day)
        priceChange= stockPrice-previousPrice
        percentChange=priceChange/stockPrice*100

    
        dateandtime = datetime.now(pytz.timezone('America/Los_Angeles')).strftime("%a %b %d %H:%M:%S %Z %Y")
        message=""
        message+=dateandtime+"\n"
        message+=companyName+" ("+StockSymbol+")\n"
        message+=str(stockPrice)+" +" if priceChange >= 0 else "-"+str(abs(round(priceChange,2)))+" (+" if percentChange >= 0 else "(-" +str(abs(round(percentChange,2)))+"%)"
        return(message)
    except EOFError as e:
        return("End Reached.")
    except ConnectionError:
        return("Network not available. Check your connection.")
    except Exception as e:
        return("Details Unavailable. Check your input\n",e)
        # break


    return 'Hello, World!'