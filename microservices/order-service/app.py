from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/orders")
def get_orders():
    return jsonify({"orders": ["order1", "order2", "order3"]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
