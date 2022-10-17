from flask import Flask, request, Blueprint, jsonify
import ultra_aquarius_api as ua

api = Blueprint("api", __name__, url_prefix="/api")

@api.route("/start_session", methods=["POST"])
def start_session():
    payload = request.json
    session_name = payload.get("sessionName")
    
    message = "Session name did not match!"
    if session_name == "iTBS-ms":
        message = "iTBS-ms session matched."
        ua.sample_session()
        message = "Completed iTBS-ms session."

    return jsonify({"message": message})

@api.route("/stop_session", methods=["GET"])
def stop_session():
    ua.stop()
    return jsonify({"message": "Session stopped."})

app = Flask(__name__)
app.register_blueprint(api)

@app.route("/", methods=["GET"])
def root():
    return "Ultra Aquarius API is running!"

if __name__ == "__main__":
    app.run(port=8889)