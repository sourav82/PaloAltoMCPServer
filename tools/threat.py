
from fastmcp import FastMCP
from app.context import MCPContext
from app.panorama_client import PanoramaClient
from services.session_store import update_session

mcp = FastMCP("paloalto-mcp")
client = PanoramaClient()


@mcp.tool()
def search_threat_logs(
    context: MCPContext,
    src_ip: str = None,
    dst_ip: str = None
):
    filters = []

    if src_ip:
        filters.append(f"(addr.src in {src_ip})")

    if dst_ip:
        filters.append(f"(addr.dst in {dst_ip})")

    query = " and ".join(filters)

    raw = client.query_logs(query, "threat")

    result = {
        "session_id": context.session_id,
        "threat_count": len(raw.get("entry", []))
    }

    update_session(context.session_id, {"threat": result})

    return result
