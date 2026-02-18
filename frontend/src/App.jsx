import { useEffect, useState } from "react";
import LaunchPad from "./components/LaunchPad";
import "./App.css";

function App() {
  const [tools, setTools] = useState([]);

  useEffect(() => {
    fetch("/api/tools")
      .then((res) => res.json())
      .then(setTools)
      .catch((err) => console.error("載入工具清單失敗:", err));
  }, []);

  return (
    <div className="app">
      <header className="app-header">
        <h1 className="app-title">台股工具集</h1>
        <p className="app-subtitle">選擇下方工具開始使用</p>
      </header>
      <main>
        <LaunchPad tools={tools} />
      </main>
    </div>
  );
}

export default App;
