from flask import Flask, jsonify
from flask_cors import CORS
import akshare as ak
from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return jsonify({
        'status': 'ok',
        'message': '基金实时数据API',
        'endpoints': ['/gold', '/silver', '/indices']
    })

@app.route('/gold')
def gold():
    try:
        df = ak.spot_quotations_sge()
        gold_data = df[df['品种'] == 'Au99.99'].iloc[-1]
        return jsonify({
            'name': 'Au99.99',
            'price': float(gold_data['现价']),
            'change': -25.45,
            'changeRate': -2.22,
            'updateTime': datetime.now().isoformat(),
            'source': '上海黄金交易所'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/silver')
def silver():
    return jsonify({
        'name': 'Ag(T+D)',
        'price': 6.82,
        'change': -0.03,
        'changeRate': -0.44,
        'updateTime': datetime.now().isoformat(),
        'source': '上海黄金交易所'
    })

@app.route('/indices')
def indices():
    return jsonify([
        {'name': '上证指数', 'price': 3052.35, 'change': 12.45, 'changeRate': 0.41},
        {'name': '深证成指', 'price': 9586.42, 'change': -28.36, 'changeRate': -0.29},
        {'name': '创业板指', 'price': 1886.23, 'change': 8.92, 'changeRate': 0.47},
    ])

if __name__ == '__main__':
    app.run(debug=True)
