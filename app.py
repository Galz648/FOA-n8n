from flask import Flask, request, jsonify
from datetime import datetime
import logging
from flask_cors import CORS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


@app.route("/test", methods=["POST"])
def test_endpoint():
    logger.info("Received POST request to /test endpoint")
    data = request.get_json()
    timestamp = datetime.now().isoformat()

    response = {
        "message": "Received data successfully",
        "timestamp": timestamp,
        "received_data": data,
    }

    logger.info(f"Request data: {data}")
    logger.info(f"Sending response: {response}")
    return jsonify(response), 200


@app.route("/", methods=["GET"])
def health_check():
    logger.info("Received GET request to health check endpoint")
    return jsonify({"status": "healthy", "message": "Flask server is running"}), 200


if __name__ == "__main__":
    logger.info("Starting Flask server...")
    app.run(host="0.0.0.0", port=5001, debug=True)
