import "./ToolCard.css";

function ToolCard({ tool }) {
  return (
    <a className="tool-card" href={tool.route}>
      <span className="tool-card-icon">{tool.icon}</span>
      <h3 className="tool-card-name">{tool.name}</h3>
      <p className="tool-card-desc">{tool.description}</p>
    </a>
  );
}

export default ToolCard;
