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

def is_engaged(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    
    for face in faces:
        landmarks = predictor(gray, face)
        landmarks = face_utils.shape_to_np(landmarks)
        
        left_eye = landmarks[42:48]
        right_eye = landmarks[36:42]
        
        left_eye_ratio = eye_aspect_ratio(left_eye)
        right_eye_ratio = eye_aspect_ratio(right_eye)
        eye_ratio = (left_eye_ratio + right_eye_ratio) / 2.0
        
        if eye_ratio < 0.2:
            print("Not Engaged (Eyes Closed)")
            return "Not Engaged (Eyes Closed)"
        
        face_direction = face_orientation(landmarks)
        if face_direction == "Front":
            print("Engaged (Looking at Camera)")
            return "Engaged (Looking at Camera)"
            
        else:
            print("Not Engaged (Looking Away)")
            return "Not Engaged (Looking Away)"
    print("No Face Detected")
    return "No Face Detected"

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
        metadata_filename = filename.replace(".jpg", ".txt")
        
        with open(metadata_filename, "w") as f:
            f.write(f"Engagement: {engagement_status}\n")
        
        return jsonify({"message": "Image and annotation saved successfully", "filename": filename, "engagement_status": engagement_status})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")
