from flask import Flask, request, jsonify
from datetime import datetime
import logging
from tiktok import get_video_analysis

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)


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


@app.route("/tiktok/video/analysis", methods=["POST"])
def tiktok_video():
    logger.info(f"Received POST request to /tiktok/video/analysis endpoint")
    data = request.get_json()
    logger.info(f"Request data: {data}")

    # Get video_url from query parameters, fallback to TikTok URL if not provided
    video_url = request.args.get("video_url")

    classification_result = get_video_analysis(
        video_url=video_url,
        prompt="summarize this video and tell if it is antisemitic or not",
        model_name="gemini-2.0-flash",
    )

    return (
        jsonify(
            {
                "status": "received",
                "message": f"Video URL: {video_url}",
                "classification_result": classification_result,
            }
        ),
        200,
    )


if __name__ == "__main__":
    logger.info("Starting Flask server...")
    app.run(host="0.0.0.0", port=5001, debug=True)
