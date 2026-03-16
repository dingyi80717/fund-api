from flask import Flask, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

FUND_CODES = [
    "008999", "011040", "014143", "014711", "003579", "502023", "004513", "019090",
    "015832", "021733", "020481", "000216", "017071", "008282", "020628", "009033",
    "014661", "015968", "009504", "013817", "008986", "020464", "021445", "011036",
    "005693", "005583"
]

@app.route("/funds")
def get_funds():
    funds_data = []
    for code in FUND_CODES:
        try:
            url = f"http://fundgz.1234567.com.cn/js/{code}.js"
            resp = requests.get(url, timeout=5)
            if resp.status_code == 200:
                text = resp.text
                json_str = text[text.find("(")+1:text.rfind(")")]
                data = eval(json_str)
                funds_data.append({
                    "code": code,
                    "name": data.get("name", ""),
                    "nav": float(data.get("dwjz", 0)),
                    "estNav": float(data.get("gsz", 0)),
                    "changeRate": float(data.get("gszzl", 0)),
                    "updateTime": data.get("gztime", ""),
                    "status": "ok"
                })
        except:
            pass
    return jsonify({"status": "ok", "funds": funds_data})

@app.route("/")
def index():
    return jsonify({"status": "ok", "endpoints": ["/funds", "/gold", "/silver"]})

@app.route("/gold")
def gold():
    return jsonify({"name": "Au99.99", "price": 508.50, "change": 0, "changeRate": 0})

@app.route("/silver")
def silver():
    return jsonify({"name": "Ag(T+D)", "price": 6.12, "change": 0, "changeRate": 0})

if __name__ == "__main__":
    app.run(debug=True)
