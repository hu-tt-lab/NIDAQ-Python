from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/start", methods=["POST"])
def start():
    data = request.json
    response = jsonify({"hello": "world" + data["this"]})
    return response

if __name__ == "__main__":
    app.run()