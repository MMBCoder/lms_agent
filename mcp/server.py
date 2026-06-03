from mcp.server.fastmcp import FastMCP

mcp = FastMCP('lms-agent')

@mcp.tool()
def health_check() -> str:
    return 'LMS Agent MCP Server Running'

if __name__ == '__main__':
    mcp.run()
