import { useState } from "react";
import { Link } from "react-router-dom";
import "./DividendCalculator.css";

function DividendCalculator() {
  const [shares, setShares] = useState("");
  const [dividend, setDividend] = useState("");
  const [transferFee, setTransferFee] = useState("10");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const handleCalculate = async (e) => {
    e.preventDefault();
    setError("");
    setResult(null);

    try {
      const res = await fetch("/api/tools/dividend/calculate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          shares: parseInt(shares, 10),
          dividend: parseFloat(dividend),
          transfer_fee: parseInt(transferFee, 10),
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
    value.toLocaleString("zh-TW", { minimumFractionDigits: 0, maximumFractionDigits: 3 });

  return (
    <div className="calculator-page">
      <Link to="/" className="back-link">&larr; 返回 Launch Pad</Link>
      <h2 className="calculator-title">股利計算器</h2>

      <form className="calculator-form" onSubmit={handleCalculate}>
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
          每股股利（元）
          <input
            type="number"
            step="0.001"
            min="0.001"
            value={dividend}
            onChange={(e) => setDividend(e.target.value)}
            required
            className="form-input"
            placeholder="例：2.555"
          />
        </label>

        <label className="form-label">
          匯費（元）
          <input
            type="number"
            step="1"
            min="0"
            value={transferFee}
            onChange={(e) => setTransferFee(e.target.value)}
            required
            className="form-input"
            placeholder="預設：10"
          />
        </label>

        <button type="submit" className="calculate-btn">計算股利</button>
      </form>

      {error && <p className="calc-error">{error}</p>}

      {result && (
        <div className="calc-result">
          <div className="result-row">
            <span className="result-label">持有股數</span>
            <span className="result-value">{formatMoney(result.shares)} 股</span>
          </div>
          <div className="result-row">
            <span className="result-label">每股股利</span>
            <span className="result-value">{formatMoney(result.dividend)} 元</span>
          </div>

          <hr className="result-divider" />

          <div className="result-row">
            <span className="result-label">股利總金額</span>
            <span className="result-value">{formatMoney(result.total)} 元</span>
          </div>
          <div className="result-row fee-row">
            <span className="result-label">匯費</span>
            <span className="result-value fee-value">-{formatMoney(result.transfer_fee)} 元</span>
          </div>

          <hr className="result-divider" />

          <div className="result-row">
            <span className="result-label">實收金額</span>
            <span className="result-value result-highlight profit">
              {formatMoney(result.net)} 元
            </span>
          </div>
        </div>
      )}
    </div>
  );
}

export default DividendCalculator;
