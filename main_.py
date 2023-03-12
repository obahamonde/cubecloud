import functions_framework
from flask import Flask, jsonify, Request, Response

app = Flask(__name__)


@app.route("/")
def hello():
    return jsonify({"message": "Hello World!"})


@functions_framework.http
def handler(req: Request) -> Response:
    with app.test_request_context(
        req.path, method=req.method, data=req.data, query_string=req.query_string
    ):
        return app.full_dispatch_request()
