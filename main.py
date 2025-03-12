from flask import Flask, request, jsonify, render_template
from firebase_admin import credentials, firestore, initialize_app
import os
from dotenv import load_dotenv

# 🔹 Initialize Flask app
app = Flask(__name__)
load_dotenv()
FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY")
FIREBASE_AUTH_DOMAIN=os.getenv("FIREBASE_AUTH_DOMAIN")
# 🔹 Initialize Firebase Admin SDK
cred = credentials.Certificate("serviceAccountKey.json")  # Your Firebase credentials file
initialize_app(cred)
db = firestore.client()

# 🔹 Route for input page
@app.route("/")
def home():
    return render_template("input.html")

# 🔹 Route to handle submitted data
@app.route("/submit", methods=["POST"])
def submit():
    data = request.json
    print("📩 Received JSON:", data)  # Debugging print

    text = data.get("text", "")
    if text:
        doc_ref = db.collection("messages").document("latest")
        doc_ref.set({"text": text})  # Store in Firestore
        print("✅ Stored in Firestore:", {"text": text})  # Debugging print
        return jsonify({"message": "Data updated!"}), 200

    print("⚠️ No text provided in request.")  # Debugging print
    return jsonify({"error": "No text provided"}), 400

# 🔹 Route for output page
@app.route("/output")
def output():
    return render_template("output.html", firebase_api_key=FIREBASE_API_KEY,firebase_auth_domain=FIREBASE_AUTH_DOMAIN)


if __name__ == "__main__":
    app.run(debug=True)
