from flask import Flask, jsonify, request
from datetime import datetime, timedelta
from flask_cors import CORS
import random
import yfinance as yf

app = Flask(__name__)
CORS(app)

# Sample data for stock suggestions
stock_suggestions = {
    'Ethical_Investing': ['AAPL', 'ADBE', 'NSRGY'],
    'Growth_Investing': ['GOOGL', 'AMZN', 'TSLA'],
    'Index_Investing': ['VTI', 'IXUS', 'ILTB'],
    'Quality_Investing': ['MSFT', 'V', 'MA'],
    'Value_Investing': ['JPM', 'WMT', 'KO']
}


@app.route('/get_stock_suggestions', methods=['POST'])
def get_stock_suggestions():
    try:
        data = request.json
        investment_amount = float(data.get('investmentAmount', 5000))
        selected_strategies = data.get('selectedStrategies', [])

        value_split=[0.6,0.3,0.1]
        # Randomly select stocks based on selected strategies
        suggested_stocks = {}
        count=1
        strategycount=len(selected_strategies)
        for strategy in selected_strategies:
            stockinfo={}
            stockdata=[]
            if strategy in stock_suggestions:
                stockinfo["name"]=strategy
                allstocks=random.sample(stock_suggestions[strategy], 3)
                for pos,eachstock in enumerate(allstocks):

                    stockdets = yf.Ticker(eachstock)
                    info = stockdets.info
                    
                    completeinfo={}
                    completeinfo["shortname"]=eachstock
                    completeinfo["value"]=(investment_amount*value_split[pos])/strategycount

                    if 'longName' in info and 'currentPrice' in info:
                        completeinfo["name"]=info['longName']
                        completeinfo["current_value"]=round(info['currentPrice'],2)
                    else:
                        completeinfo["name"]=info['longName']
                        completeinfo["current_value"]=round(info['navPrice'],2)
                    
                    end_date = datetime.now()
                    start_date = end_date - timedelta(days=10)
                    historical_data = stockdets.history(start=start_date, end=end_date)
                    closing_prices = round(historical_data['Close'].tail(5),2)
                    completeinfo["history"]=(list(closing_prices))
                    stockdata.append(completeinfo)
                    
                stockinfo["stocks"]=stockdata
                suggested_stocks["strategy"+str(count)] = stockinfo
                count+=1

        # Simulate money division (equal amount for each stock)

        return jsonify(suggested_stocks)

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': 'Internal Server Error'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000, debug=True)
