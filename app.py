import logging
import os
from datetime import datetime, timezone
from flask import Flask, jsonify, request

# Config logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt="%Y-%m-%dT%H:%M:%S%z",
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.before_request
def log_request():
    logger.info("%s %s from %s", request.method, request.path, request.remote_addr)

@app.route("/")
def index():
    return jsonify(
        {
            "service": "cloud-task",
            "status": "good to go",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    )

@app.route("/health")
def health():
    return jsonify(
        {
            "status:": "healthy"
        }
    ), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(
        host="0.0.0.0",
        port=port,
        ssl_context=("/certs/cert.pem", "/certs/key.pem"),
    )