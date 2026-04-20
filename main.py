
from fastmcp import FastMCP

# import tools so decorators register
from tools import traffic, threat

mcp = FastMCP("paloalto-mcp")

if __name__ == "__main__":
    mcp.run()
