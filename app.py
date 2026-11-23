from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

client = MongoClient(
    "mongodb://localhost:27017/",
    serverSelectionTimeoutMS=3000
)
db = client["nosql_injection_demo"]

vulnerable_users = db["vulnerable_users"]
secure_users = db["secure_users"]

DEMO_USERNAME = "admin"
DEMO_PASSWORD = "Admin@123"


def create_demo_users():
    vulnerable_users.update_one(
        {"username": DEMO_USERNAME},
        {"$set": {
            "username": DEMO_USERNAME,
            "password": DEMO_PASSWORD
        }},
        upsert=True
    )

    secure_users.update_one(
        {"username": DEMO_USERNAME},
        {"$set": {
            "username": DEMO_USERNAME,
            "password_hash": generate_password_hash(DEMO_PASSWORD)
        }},
        upsert=True
    )


@app.route("/")
def home():
    return render_template(
        "index.html",
        demo_username=DEMO_USERNAME,
        demo_password=DEMO_PASSWORD
    )


@app.route("/api/vulnerable-login", methods=["POST"])
def vulnerable_login():
    data = request.get_json()

    if not isinstance(data, dict):
        return jsonify({"success": False, "message": "Invalid request."}), 400

    username = data.get("username")
    password = data.get("password")

    # The input is used directly in the MongoDB query.
    user = vulnerable_users.find_one({
        "username": username,
        "password": password
    })

    if user:
        return jsonify({
            "success": True,
            "message": "Login successful. The query accepted the input."
        })

    return jsonify({
        "success": False,
        "message": "Username or password is incorrect."
    }), 401


@app.route("/api/secure-login", methods=["POST"])
def secure_login():
    data = request.get_json()

    if not isinstance(data, dict):
        return jsonify({"success": False, "message": "Invalid request."}), 400

    username = data.get("username")
    password = data.get("password")

    if not isinstance(username, str) or not isinstance(password, str):
        return jsonify({
            "success": False,
            "message": "Username and password must be strings."
        }), 400

    user = secure_users.find_one({"username": username})

    if user and check_password_hash(user["password_hash"], password):
        return jsonify({
            "success": True,
            "message": "Login successful. Password is correct."
        })

    return jsonify({
        "success": False,
        "message": "Username or password is incorrect."
    }), 401


if __name__ == "__main__":
    try:
        client.admin.command("ping")
        create_demo_users()
        print("MongoDB connected.")
        print("Demo account: admin / Admin@123")
        print("Open http://127.0.0.1:5000")
        app.run(host="127.0.0.1", port=5000, debug=False)
    except Exception as error:
        print("Cannot connect to MongoDB. Please start MongoDB first.")
        print(error)
