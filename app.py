from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)


@app.route("/test", methods=["POST"])
def test_endpoint():
    data = request.get_json()
    timestamp = datetime.now().isoformat()

    response = {
        "message": "Received data successfully",
        "timestamp": timestamp,
        "received_data": data,
    }

    print(f"Received request with data: {data}")  # Added logging
    return jsonify(response), 200


@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy", "message": "Flask server is running"}), 200


if __name__ == "__main__":
    print("Starting Flask server...")  # Added startup logging
    app.run(port=5001, debug=True)
