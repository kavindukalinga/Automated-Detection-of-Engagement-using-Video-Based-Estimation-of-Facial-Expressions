import React, { useRef, useEffect, useState } from "react";
import Webcam from "react-webcam";

const WebcamCapture: React.FC = () => {
  const webcamRef = useRef<Webcam>(null);
  const [capturing, setCapturing] = useState<boolean>(true);

  // Function to capture an image and send it to the backend
  const captureAndSend = async () => {
    if (webcamRef.current) {
      const imageSrc = webcamRef.current.getScreenshot();
      if (imageSrc) {
        try {

          const response1 = await fetch("http://127.0.0.1:5000/users");
          const data1 = await response1.json();


          const response = await fetch("http://127.0.0.1:5000/data", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ image: imageSrc, userId:data1.userId, courseId:data1.courseId }),
          });
          const data = await response.json();
          console.log("Server response:", data);
        } catch (error) {
          console.error("Error sending image:", error);
        }
      }
    }
  };

  useEffect(() => {
    // let interval: NodeJS.Timeout | undefined;
    let interval: number | undefined;

    
    if (capturing) {
      interval = setInterval(() => {
        captureAndSend();
      }, 6000); // Capture every 60 seconds
    } else {
      // Stop the webcam when capturing is false
      if (webcamRef.current && webcamRef.current.video) {
        const stream = webcamRef.current.video.srcObject as MediaStream;
        if (stream) {
          stream.getTracks().forEach((track) => track.stop()); // Stop all tracks
        }
      }
    }

    return () => {
      if (interval) clearInterval(interval); // Cleanup interval on unmount
    };
  }, [capturing]);

  return (
    <div className="flex flex-col items-center justify-center">
      {capturing && (
        <Webcam
          audio={false}
          ref={webcamRef}
          screenshotFormat="image/jpeg"
          className="w-96 h-64 border border-gray-300 rounded-lg"
          style={{
            visibility: "hidden", // Hides it but keeps rendering
            position: "absolute", 
            // width: "200px", // Maintain a small size
            // height: "150px",
          }}
        />
      )}
      <button
        onClick={() => setCapturing((prev) => !prev)}
        className="mt-4 p-2 bg-blue-500 text-white rounded"
      >
        {capturing ? "Stop Capture" : "Start Capture"}
      </button>
    </div>
  );
};

export default WebcamCapture;
