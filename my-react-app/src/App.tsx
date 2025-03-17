import React from "react";
import HelloWorld from "./components/HelloWorld";
import WebcamCapture from "./components/WebcamCapture";

const App: React.FC = () => {
  return (
    <div className="flex items-center justify-center h-screen">
      <HelloWorld />
      <WebcamCapture />
    </div>
  );
};

export default App;