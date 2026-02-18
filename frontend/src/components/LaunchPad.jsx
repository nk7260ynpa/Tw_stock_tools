import ToolCard from "./ToolCard";
import "./LaunchPad.css";

function LaunchPad({ tools }) {
  if (tools.length === 0) {
    return <p className="launchpad-empty">尚未新增任何工具</p>;
  }

  return (
    <div className="launchpad-grid">
      {tools.map((tool) => (
        <ToolCard key={tool.id} tool={tool} />
      ))}
    </div>
  );
}

export default LaunchPad;
