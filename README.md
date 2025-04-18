# Finage MCP Server

A MCP server for the stock market data API, Finage API.
Only small subset of endpoints is implemented.

### Warning
The package is under development and only supports two endpoint as of v0.0.1. Be cautious.

## Configuration

### Getting an API Key
1. Sign up for a [Free Finage API key](https://finage.co.uk/)
2. Add the API key to your environment variables as `FINAGE_API_KEY`
3. Make sure you have `uv` installed


## Clone the project

```bash
git clone https://github.com/KendamaQQ/finage_mcp.git
```

### Usage with Claude Desktop
Add this to your `claude_desktop_config.json`:

**NOTE** Make sure you replace the `<DIRECTORY-OF-CLONED-PROJECT>` with the directory of the cloned project.

```
{
  "mcpServers": {
    "finage_mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "<DIRECTORY-OF-CLONED-PROJECT>/finage_mcp",
        "run",
        "finage_mcp"
      ],
      "env": {
        "FINAGE_API_KEY": "YOUR_API_KEY_HERE"
      }
    }
  }
}
```
