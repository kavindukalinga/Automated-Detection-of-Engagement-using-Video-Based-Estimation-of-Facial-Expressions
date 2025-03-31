from flask import Flask, request, jsonify
import base64
import os
from datetime import datetime
from flask_cors import CORS
import cv2
import numpy as np
import dlib
from imutils import face_utils

app = Flask(__name__)

CORS(app)


UPLOAD_FOLDER = "captured_images"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def is_engaged(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    if len(faces) == 0:
        return "No Face Detected"
    
    for (x, y, w, h) in faces:
        face_roi = gray[y:y+h, x:x+w]
        eyes_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")
        eyes = eyes_cascade.detectMultiScale(face_roi)
        
        if len(eyes) >= 1:
            return "Engaged (Looking at Camera)"
        else:
            return "Not Engaged (Eyes Closed or Looking Away)"
    
    return "Not Engaged"


def eye_aspect_ratio(eye):
    A = np.linalg.norm(eye[1] - eye[5])
    B = np.linalg.norm(eye[2] - eye[4])
    C = np.linalg.norm(eye[0] - eye[3])
    return (A + B) / (2.0 * C)

def face_orientation(landmarks):
    nose_tip = landmarks[30]
    chin = landmarks[8]
    left_cheek = landmarks[1]
    right_cheek = landmarks[15]
    
    face_width = np.linalg.norm(left_cheek - right_cheek)
    face_height = np.linalg.norm(nose_tip - chin)
    aspect_ratio = face_width / face_height
    
    if 0.9 < aspect_ratio < 1.1:
        return "Front"
    else:
        return "Side"


@app.route("/")
def hello():
    return jsonify({"Hello":" World!"})

@app.route("/users",methods=["GET","POST"])
def getUsers():
    return jsonify({"userId":"nuwan","courseId":2302 })

@app.route("/data",methods=["POST"])
def incomingData():
    data=request.get_json()
    print(data.get("userId"), data.get("courseId"))
    # print(data.get("image"))
    image_data = data.get("image")

    if not image_data:
        return jsonify({"error": "No image data received"}), 400

    image_data = image_data.split(",")[1]
    image_bytes = base64.b64decode(image_data)
    with open("imageTextK.txt", "wb") as f:
        f.write(image_bytes)
    return jsonify(data)

@app.route("/upload", methods=["POST"])
def upload_image():
    print("Request received")
    try:
        data = request.get_json()
        image_data = data.get("image")

        if not image_data:
            return jsonify({"error": "No image data received"}), 400

        image_data = image_data.split(",")[1]
        image_bytes = base64.b64decode(image_data)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{UPLOAD_FOLDER}/capture_{timestamp}.jpg"
        
        with open(filename, "wb") as f:
            f.write(image_bytes)
        
        engagement_status = is_engaged(filename)
        print(engagement_status)
        metadata_filename = filename.replace(".jpg", ".txt")
        
        with open(metadata_filename, "w") as f:
            f.write(f"Engagement: {engagement_status}\n")
        
        return jsonify({"message": "Image and annotation saved successfully", "filename": filename, "engagement_status": engagement_status})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")
