from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__, static_folder='frontend')

# Serve static files
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder + '/html', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

# API endpoints
prices = {
    "bier": {"price": 2.5, "sales": 0},
    "wit": {"price": 3.0, "sales": 0},
}

@app.route('/api/prices', methods=['GET', 'POST'])
def handle_prices():
    if request.method == 'POST':
        data = request.json
        for drink, info in data.items():
            prices[drink] = info
        return jsonify({"message": "Prices updated"}), 200
    return jsonify(prices), 200

@app.route('/api/sales', methods=['POST'])
def update_sales():
    data = request.json
    for drink, sales in data.items():
        if drink in prices:
            prices[drink]["sales"] += sales
    return jsonify({"message": "Sales updated"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)