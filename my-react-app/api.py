from datetime import datetime
from flask import Flask, request, jsonify
import base64
import cv2
import numpy as np
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "capturedImages"
finalEngagementStatus=0
engarray=[]
# face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
# eyes_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

# def is_engaged(image_bytes):
#     nparr = np.frombuffer(image_bytes, np.uint8)
#     image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
#     if len(faces) == 0:
#         return "No Face Detected"
    
#     for (x, y, w, h) in faces:
#         face_roi = gray[y:y+h, x:x+w]
#         eyes = eyes_cascade.detectMultiScale(face_roi)
#         print(len(eyes))
#         if len(eyes) >= 0.5:
            
#             return "Engaged (Looking at Camera)"
#         else:
#             return "Not Engaged (Eyes Closed or Looking Away)"
    
#     return "Not Engaged"

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye_tree_eyeglasses.xml")

def is_engaged(image_bytes):
    nparr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(30, 30))
    
    if len(faces) == 0:
        return "No Face Detected"
    
    for (x, y, w, h) in faces:
        face_roi = gray[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(face_roi, scaleFactor=1.1, minNeighbors=1, minSize=(15, 15))
        print(len(eyes))
        if len(eyes) >= 1:
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
        
        # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # print(timestamp)
        # filename = f"{UPLOAD_FOLDER}/capture_{timestamp}.jpg"
        
        # with open(filename, "wb") as f:
        #     f.write(image_bytes)
        global finalEngagementStatus
        global engarray
        engagement_status = is_engaged(image_bytes)
        
        engarray.append(engagement_status)
        if engagement_status=="Engaged (Looking at Camera)": 
            finalEngagementStatus = 2
        elif engagement_status=="Not Engaged (Eyes Closed or Looking Away)" and finalEngagementStatus==0:
            finalEngagementStatus = 1
        if len(engarray)==10:
            print("Engagement Status: ",finalEngagementStatus) # send to database
            
            finalEngagementStatus=0
            engarray=[]
        print(engagement_status)
        
        return jsonify({"engagement_status": engagement_status})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
