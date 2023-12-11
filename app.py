from flask import Flask, jsonify, request
from datetime import datetime, timedelta
from flask_cors import CORS
import random
import yfinance as yf

app = Flask(__name__)
CORS(app)

# Sample data for stock suggestions
fixed_stock_suggestions = {
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
        suggested_stocks = {}
        count=1
        strategycount=len(selected_strategies)
        for strategy in selected_strategies:
            complete_strategy_info={}
            stockdata=[]
            if strategy in fixed_stock_suggestions:
                complete_strategy_info["name"]=strategy
                all_stocks=random.sample(fixed_stock_suggestions[strategy], 3)
                for position,each_stock in enumerate(all_stocks):

                    stock_details = yf.Ticker(each_stock)
                    info = stock_details.info
                    
                    complete_stock_info={}
                    complete_stock_info["shortname"]=each_stock
                    complete_stock_info["value"]=(investment_amount*value_split[position])/strategycount
                    complete_stock_info["name"]=info['longName']

                    if 'longName' in info and 'currentPrice' in info:
                        complete_stock_info["current_value"]=round(info['currentPrice'],2)
                    else:
                        complete_stock_info["current_value"]=round(info['navPrice'],2)
                    
                    end_date = datetime.now()
                    start_date = end_date - timedelta(days=10)
                    historical_data = stock_details.history(start=start_date, end=end_date)
                    closing_prices = round(historical_data['Close'].tail(5),2)
                    complete_stock_info["history"]=(list(closing_prices))
                    stockdata.append(complete_stock_info)
                    
                complete_strategy_info["stocks"]=stockdata
                suggested_stocks["strategy"+str(count)] = complete_strategy_info
                count+=1

        # Simulate money division (equal amount for each stock)

        return jsonify(suggested_stocks)

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': 'Internal Server Error'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000, debug=True)
