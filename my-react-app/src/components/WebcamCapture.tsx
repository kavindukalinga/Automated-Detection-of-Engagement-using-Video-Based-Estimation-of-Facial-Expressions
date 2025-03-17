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
          const response = await fetch("http://127.0.0.1:5000/upload", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ image: imageSrc }),
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
    if (capturing) {
      const interval = setInterval(() => {
        captureAndSend();
      }, 6000); // Capture every 60 seconds

      return () => clearInterval(interval); // Cleanup interval on unmount
    }
  }, [capturing]);

  return (
    <div className="flex flex-col items-center justify-center">
      <Webcam
        audio={false}
        ref={webcamRef}
        screenshotFormat="image/jpeg"
        className="w-96 h-64 border border-gray-300 rounded-lg"
        // style={{ display: "none" }} // Hides the video feed
        // style={{ width: 0, height: 0, position: "absolute" }} // Keeps it functional but hidden
        // style={{
        //   position: "absolute",
        //   top: "-9999px", // Moves it off-screen
        //   opacity: 0, // Makes it invisible
        //   pointerEvents: "none", // Prevents interactions
        // }}
        style={{
          visibility: "hidden", // Hides it but keeps rendering
          position: "absolute", 
          // width: "200px", // Maintain a small size
          // height: "150px",
        }}
      />
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
