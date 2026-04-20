
from fastmcp import FastMCP
from app.context import MCPContext
from app.panorama_client import PanoramaClient
from app.parser import parse_traffic_logs
from services.session_store import update_session

mcp = FastMCP("paloalto-mcp")
client = PanoramaClient()


@mcp.tool()
def search_traffic_logs(
    context: MCPContext,
    src_ip: str = None,
    dst_ip: str = None,
    port: int = None,
    action: str = None
):
    filters = []

    if src_ip:
        filters.append(f"(addr.src in {src_ip})")

    if dst_ip:
        filters.append(f"(addr.dst in {dst_ip})")

    if port:
        filters.append(f"(port.dst eq {port})")

    if action:
        filters.append(f"(action eq {action})")

    query = " and ".join(filters)

    raw = client.query_logs(query, "traffic")
    parsed = parse_traffic_logs(raw)

    decision = "unknown"
    if any(l["action"] == "deny" for l in parsed):
        decision = "deny"
    elif any(l["action"] == "allow" for l in parsed):
        decision = "allow"

    result = {
        "session_id": context.session_id,
        "count": len(parsed),
        "decision": decision,
        "logs": parsed[:50]
    }

    update_session(context.session_id, {"traffic": result})

    return result
