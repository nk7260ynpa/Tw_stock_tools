import { useState, useEffect, useMemo } from "react";
import { Link } from "react-router-dom";
import "./KnowledgeBase.css";

function KnowledgeBase() {
  const [knowledgeData, setKnowledgeData] = useState([]);
  const [categories, setCategories] = useState(["全部"]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState("");
  const [activeCategory, setActiveCategory] = useState("全部");
  const [openItems, setOpenItems] = useState(new Set());

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);
      try {
        const [dataRes, catRes] = await Promise.all([
          fetch("/api/tools/knowledge"),
          fetch("/api/tools/knowledge/categories"),
        ]);
        const data = await dataRes.json();
        const cats = await catRes.json();
        setKnowledgeData(data);
        setCategories(["全部", ...cats]);
      } catch (err) {
        console.error("載入知識庫失敗:", err);
        setError("無法載入知識庫資料，請稍後再試。");
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const filteredData = useMemo(() => {
    return knowledgeData.filter((item) => {
      const matchCategory =
        activeCategory === "全部" || item.category === activeCategory;
      const keyword = searchTerm.trim().toLowerCase();
      const matchSearch =
        !keyword ||
        item.term.toLowerCase().includes(keyword) ||
        item.description.toLowerCase().includes(keyword);
      return matchCategory && matchSearch;
    });
  }, [knowledgeData, searchTerm, activeCategory]);

  const toggleItem = (index) => {
    setOpenItems((prev) => {
      const next = new Set(prev);
      if (next.has(index)) {
        next.delete(index);
      } else {
        next.add(index);
      }
      return next;
    });
  };

  const expandAll = () => {
    setOpenItems(new Set(filteredData.map((_, i) => i)));
  };

  const collapseAll = () => {
    setOpenItems(new Set());
  };

  const renderDescription = (text) => {
    const parts = text.split(/【([^】]+)】/);
    if (parts.length <= 1) {
      return <p className="knowledge-item-desc">{text}</p>;
    }
    return (
      <div className="knowledge-item-desc">
        {parts[0] && <p className="knowledge-desc-intro">{parts[0]}</p>}
        {Array.from({ length: Math.floor((parts.length - 1) / 2) }, (_, i) => (
          <div key={i} className="knowledge-desc-section">
            <h4 className="knowledge-desc-section-title">{parts[i * 2 + 1]}</h4>
            <p className="knowledge-desc-section-content">{parts[i * 2 + 2]}</p>
          </div>
        ))}
      </div>
    );
  };

  if (loading) {
    return (
      <div className="knowledge-page">
        <Link to="/" className="back-link">&larr; 返回 Launch Pad</Link>
        <h2 className="knowledge-title">台股知識庫</h2>
        <p className="knowledge-subtitle">資料載入中...</p>
      </div>
    );
  }

  return (
    <div className="knowledge-page">
      <Link to="/" className="back-link">&larr; 返回 Launch Pad</Link>
      <h2 className="knowledge-title">台股知識庫</h2>
      <p className="knowledge-subtitle">台股交易規則、費用稅務與實用公式速查</p>

      {error && <p className="knowledge-empty">{error}</p>}

      <div className="knowledge-search">
        <input
          type="text"
          className="knowledge-search-input"
          placeholder="搜尋術語或說明..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </div>

      <div className="knowledge-tabs">
        {categories.map((cat) => (
          <button
            key={cat}
            type="button"
            className={`knowledge-tab ${activeCategory === cat ? "active" : ""}`}
            onClick={() => {
              setActiveCategory(cat);
              setOpenItems(new Set());
            }}
          >
            {cat}
          </button>
        ))}
      </div>

      <div className="knowledge-actions">
        <button type="button" className="knowledge-action-btn" onClick={expandAll}>全部展開</button>
        <button type="button" className="knowledge-action-btn" onClick={collapseAll}>全部收合</button>
        <span className="knowledge-count">共 {filteredData.length} 筆</span>
      </div>

      <div className="knowledge-list">
        {filteredData.length === 0 && !error && (
          <p className="knowledge-empty">目前無資料</p>
        )}
        {filteredData.map((item, index) => {
          const isOpen = openItems.has(index);
          return (
            <div className="knowledge-item" key={`${item.category}-${item.term}`}>
              <button
                type="button"
                className={`knowledge-item-header ${isOpen ? "open" : ""}`}
                onClick={() => toggleItem(index)}
              >
                <div className="knowledge-item-left">
                  <span className="knowledge-item-badge">{item.category}</span>
                  <span className="knowledge-item-term">{item.term}</span>
                </div>
                <span className="knowledge-item-arrow">{isOpen ? "\u25B2" : "\u25BC"}</span>
              </button>
              {isOpen && (
                <div className="knowledge-item-body">
                  {renderDescription(item.description)}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default KnowledgeBase;
