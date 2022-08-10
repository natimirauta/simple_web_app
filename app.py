# click counter
from flask import Flask
import logging
import socket

app = Flask(__name__)

gunicorn_error_logger = logging.getLogger('gunicorn.error')
app.logger.handlers.extend(gunicorn_error_logger.handlers)
app.logger.setLevel(logging.INFO)

@app.route("/", methods=["GET"])
def hello():
    return f"Hello from {socket.gethostname()}\n"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
