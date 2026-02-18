import { Link } from "react-router-dom";
import "./ToolCard.css";

function ToolCard({ tool }) {
  return (
    <Link className="tool-card" to={tool.route}>
      <span className="tool-card-icon">{tool.icon}</span>
      <h3 className="tool-card-name">{tool.name}</h3>
      <p className="tool-card-desc">{tool.description}</p>
    </Link>
  );
}

export default ToolCard;
