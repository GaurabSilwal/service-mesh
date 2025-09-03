from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/payments")
def get_payments():
    return jsonify({"payments": ["payment1", "payment2"]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
