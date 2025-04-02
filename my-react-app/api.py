from flask import Flask, request, jsonify
import base64
import cv2
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
eyes_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

def is_engaged(image_bytes):
    nparr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    if len(faces) == 0:
        return "No Face Detected"
    
    for (x, y, w, h) in faces:
        face_roi = gray[y:y+h, x:x+w]
        eyes = eyes_cascade.detectMultiScale(face_roi)
        print(len(eyes))
        if len(eyes) >= 0.5:
            
            return "Engaged (Looking at Camera)"
        else:
            return "Not Engaged (Eyes Closed or Looking Away)"
    
    return "Not Engaged"

@app.route("/users",methods=["GET","POST"])
def getUsers():
    return jsonify({"userId":"nuwan","courseId":2302 })

@app.route("/data", methods=["POST"])
def upload_image():
    try:
        data = request.get_json()
        image_data = data.get("image")

        if not image_data:
            return jsonify({"error": "No image data received"}), 400

        image_data = image_data.split(",")[1]
        image_bytes = base64.b64decode(image_data)
        
        engagement_status = is_engaged(image_bytes)
        print(engagement_status)
        
        return jsonify({"engagement_status": engagement_status})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
