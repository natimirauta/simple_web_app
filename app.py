# button clicker
from flask import Flask, render_template, request, make_response, g
from redis import Redis
import json
import logging
import os
import random
import socket

app = Flask(__name__)
user = os.getenv('APP_USER', "Anonymous")

gunicorn_error_logger = logging.getLogger('gunicorn.error')
app.logger.handlers.extend(gunicorn_error_logger.handlers)
app.logger.setLevel(logging.INFO)


def get_redis():
    if not hasattr(g, 'redis'):
        g.redis = Redis(host="redis", db=0, socket_timeout=5)
    return g.redis


@app.route("/", methods=["POST", "GET"])
def hello():
    clicker_id = request.cookies.get('clicker_id')
    if not clicker_id:
        clicker_id = hex(random.getrandbits(64))[2:-1]

    click = None

    if request.method == "POST":
        redis = get_redis()
        click = request.form['click']
        data = json.dumps({'clicker_id': clicker_id, 'click': click})
        redis.rpush('click', data)
        resp = make_response(render_template("clicked.html"))

    if request.method == "GET":
        resp = make_response(render_template(
            "index.html",
            user=user,
            hostname=socket.gethostname(),
        ))

    resp.set_cookie('clicker_id', clicker_id)
    return resp


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
