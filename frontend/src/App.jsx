import { useEffect, useState } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import LaunchPad from "./components/LaunchPad";
import DividendCalculator from "./pages/DividendCalculator";
import StockProfitCalculator from "./pages/StockProfitCalculator";
import TradingSchedule from "./pages/TradingSchedule";
import KnowledgeBase from "./pages/KnowledgeBase";
import TradingCalendar from "./pages/TradingCalendar";
import { apiUrl } from "./utils/api";
import "./App.css";

function Home() {
  const [tools, setTools] = useState([]);

  useEffect(() => {
    fetch(apiUrl("/api/tools"))
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

function App() {
  const basename = (import.meta.env.BASE_URL || "/").replace(/\/$/, "");
  return (
    <BrowserRouter basename={basename}>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/tools/stock-profit" element={<StockProfitCalculator />} />
        <Route path="/tools/dividend" element={<DividendCalculator />} />
        <Route path="/tools/trading-schedule" element={<TradingSchedule />} />
        <Route path="/tools/knowledge" element={<KnowledgeBase />} />
        <Route path="/tools/calendar" element={<TradingCalendar />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
