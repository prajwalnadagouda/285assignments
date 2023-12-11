from flask import Flask, jsonify, request
from flask_cors import CORS
import random

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
        print(investment_amount)
        print(selected_strategies)
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
                    completeinfo={}
                    completeinfo["name"]=eachstock
                    completeinfo["shortname"]=eachstock
                    completeinfo["value"]=(investment_amount*value_split[pos])/strategycount
                    completeinfo["current_value"]=120.2
                    completeinfo["history"]=[123,124,125,126,127]
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
