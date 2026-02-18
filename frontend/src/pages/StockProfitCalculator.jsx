import { useState } from "react";
import { Link } from "react-router-dom";
import "./StockProfitCalculator.css";

function StockProfitCalculator() {
  const [avgPrice, setAvgPrice] = useState("");
  const [shares, setShares] = useState("");
  const [currentPrice, setCurrentPrice] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const handleCalculate = async (e) => {
    e.preventDefault();
    setError("");
    setResult(null);

    try {
      const res = await fetch("/api/tools/stock-profit/calculate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          avg_price: parseFloat(avgPrice),
          shares: parseInt(shares, 10),
          current_price: parseFloat(currentPrice),
        }),
      });

      if (!res.ok) {
        const detail = await res.json();
        setError(detail.detail?.[0]?.msg || "計算失敗，請檢查輸入");
        return;
      }

      setResult(await res.json());
    } catch {
      setError("無法連線至伺服器");
    }
  };

  const formatMoney = (value) =>
    value.toLocaleString("zh-TW", { minimumFractionDigits: 0, maximumFractionDigits: 2 });

  return (
    <div className="calculator-page">
      <Link to="/" className="back-link">&larr; 返回 Launch Pad</Link>
      <h2 className="calculator-title">股票損益計算器</h2>

      <form className="calculator-form" onSubmit={handleCalculate}>
        <label className="form-label">
          購買均價（元）
          <input
            type="number"
            step="0.01"
            min="0.01"
            value={avgPrice}
            onChange={(e) => setAvgPrice(e.target.value)}
            required
            className="form-input"
            placeholder="例：50.5"
          />
        </label>

        <label className="form-label">
          持有股數
          <input
            type="number"
            step="1"
            min="1"
            value={shares}
            onChange={(e) => setShares(e.target.value)}
            required
            className="form-input"
            placeholder="例：1000"
          />
        </label>

        <label className="form-label">
          現在價格（元）
          <input
            type="number"
            step="0.01"
            min="0.01"
            value={currentPrice}
            onChange={(e) => setCurrentPrice(e.target.value)}
            required
            className="form-input"
            placeholder="例：55.0"
          />
        </label>

        <button type="submit" className="calculate-btn">計算損益</button>
      </form>

      {error && <p className="calc-error">{error}</p>}

      {result && (
        <div className="calc-result">
          <div className="result-row">
            <span className="result-label">總買入成本</span>
            <span className="result-value">{formatMoney(result.cost)} 元</span>
          </div>
          <div className="result-row">
            <span className="result-label">目前市值</span>
            <span className="result-value">{formatMoney(result.market_value)} 元</span>
          </div>

          <hr className="result-divider" />

          <div className="result-row fee-row">
            <span className="result-label">賣出手續費</span>
            <span className="result-value fee-value">-{formatMoney(result.sell_commission)} 元</span>
          </div>
          <div className="result-row fee-row">
            <span className="result-label">證交稅</span>
            <span className="result-value fee-value">-{formatMoney(result.transaction_tax)} 元</span>
          </div>
          <div className="result-row fee-row">
            <span className="result-label">總交易成本</span>
            <span className="result-value fee-value">-{formatMoney(result.total_fees)} 元</span>
          </div>

          <hr className="result-divider" />

          <div className="result-row">
            <span className="result-label">淨損益</span>
            <span className={`result-value result-highlight ${result.profit_loss >= 0 ? "profit" : "loss"}`}>
              {result.profit_loss >= 0 ? "+" : ""}{formatMoney(result.profit_loss)} 元
            </span>
          </div>
          <div className="result-row">
            <span className="result-label">報酬率</span>
            <span className={`result-value result-highlight ${result.profit_loss_pct >= 0 ? "profit" : "loss"}`}>
              {result.profit_loss_pct >= 0 ? "+" : ""}{result.profit_loss_pct}%
            </span>
          </div>
        </div>
      )}
    </div>
  );
}

export default StockProfitCalculator;
