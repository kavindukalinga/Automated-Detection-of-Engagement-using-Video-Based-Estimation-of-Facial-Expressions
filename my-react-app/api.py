from flask import Flask, request, jsonify
import base64
import os
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)

CORS(app)


UPLOAD_FOLDER = "captured_images"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def hello():
    return jsonify({"Hello":" World!"})

@app.route("/upload", methods=["POST"])
def upload_image():
    print("Request received")
    try:
        data = request.get_json()
        image_data = data.get("image")

        if not image_data:
            return jsonify({"error": "No image data received"}), 400

        # Decode base64 image
        image_data = image_data.split(",")[1]
        image_bytes = base64.b64decode(image_data)

        # Save image
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{UPLOAD_FOLDER}/capture_{timestamp}.jpg"
        with open(filename, "wb") as f:
            f.write(image_bytes)

        return jsonify({"message": "Image saved successfully", "filename": filename})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")
