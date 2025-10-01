### Prerequisites
```bash
# Install dependencies
pip install -r requirements.txt

# Install FastMCP globally (if not already installed)
pip install fastmcp
```

### COMMAND CHEATSHEET
```bash
# Run FastMCP directly for testing
SQLITE_DB_PATH=/Users/owner/claude-code/agentic-ai-learnings/hw3/sqlite-explorer-fastmcp-mcp-server/financial_data.db fastmcp run sqlite_explorer.py

# Test with inspector (if available)
SQLITE_DB_PATH=/Users/owner/claude-code/agentic-ai-learnings/hw3/sqlite-explorer-fastmcp-mcp-server/financial_data.db fastmcp inspect sqlite_explorer.py

# To install SQLite Explorer
SQLITE_DB_PATH=/Users/owner/claude-code/agentic-ai-learnings/hw3/sqlite-explorer-fastmcp-mcp-server/financial_data.db fastmcp install sqlite_explorer.py --name "SQLite Explorer"

# To launch SQLite Explorer via a web-based testing interface. Run with `--transport sse` for HTTP-based communication  
SQLITE_DB_PATH=/Users/owner/claude-code/agentic-ai-learnings/hw3/sqlite-explorer-fastmcp-mcp-server/financial_data.db fastmcp dev sqlite_explorer.py

# To set up the MCP server with Claude Desktop
SQLITE_DB_PATH=/Users/owner/claude-code/agentic-ai-learnings/hw3/sqlite-explorer-fastmcp-mcp-server/financial_data.db fastmcp claude-desktop add sqlite_explorer.py --name "SQLite Explorer"

# Need to define the SQLITE_DB_PATH variable before running smithery playground 
SQLITE_DB_PATH=/Users/owner/claude-code/agentic-ai-learnings/hw3/sqlite-explorer-fastmcp-mcp-server/financial_data.db smithery playground
```

After launching Smithery playground, we can now talk to the MCP server using this URL: https://smithery.ai/playground?mcp=https%3A%2F%2Fee09cd8f.ngrok.smithery.ai%2Fmcp

#### For VSCode with Cline
```bash
# Add this configuration to Cline MCP settings:
{
  "sqlite-explorer": {
    "command": "uv",
    "args": [
      "run",
      "--with",
      "fastmcp",
      "--with",
      "uvicorn",
      "fastmcp",
      "run",
      "/Users/owner/claude-code/agentic-ai-learnings/hw3/sqlite-explorer-fastmcp-mcp-server/sqlite_explorer.py"
    ],
    "env": {
      "SQLITE_DB_PATH": "/Users/owner/claude-code/agentic-ai-learnings/hw3/sqlite-explorer-fastmcp-mcp-server/financial_data.db"
    }
  }
}
```

#### Example output. MCP server provides four components. SQLite Explorer provides those tools.
Server
  Name:         SQLite Explorer
  Generation:   2

Components
  Tools:        3
  Prompts:      0
  Resources:    0
  Templates:    0

Environment
  FastMCP:      2.12.4
  MCP:          1.15.0

  This will open an interactive inspector where you can test the MCP tools:
  - list_tables - to see what tables are in your database
  - describe_table - to see the structure of a specific table
  - read_query - to run SELECT queries on your data


### Notes
Even though we're running the MCP locally, still have a web interface
For locally deployed MCP server SQLite Explorer, this is the MCP server URL that we can access as a client: http://localhost:6274/?MCP_PROXY_AUTH_TOKEN=e01acfa4461c1af5227669c2c0051e7cf9c280fb61a43a146a672463441f4c1b#tools
In the future, once deployed, we'll have the same thing - HTTP or HTTPS, but instead of a local host, it'll be my server and the port. The rest will be something else. 
Local host is the server name, so the server is a local host. But if deployed somewhere, then it'll be a different host name. The port serves as a channel to talk to multiple MCP servers. HTTPS is a secure HTTP. 

#### Sample Questions to Ask Your AI Assistant

Once the MCP server is connected, you can ask questions like:

- "What tables are in my database?"
- "Show me the structure of my financial data"
- "What are the first 10 rows from [table_name]?"
- "How many records are in each table?"
- "Show me all transactions over $1000"
- "What's the average amount in the transactions table?"

NOTE: The tables starting with SQLite are called system tables. We never created those tables.

### Troubleshooting

```bash
# Check FastMCP version and available commands
fastmcp --help
fastmcp version

# Verify your database file exists
ls -la /Users/owner/claude-code/agentic-ai-learnings/hw3/sqlite-explorer-fastmcp-mcp-server/financial_data.db

# Test database directly with sqlite3
sqlite3 /Users/owner/claude-code/agentic-ai-learnings/hw3/sqlite-explorer-fastmcp-mcp-server/financial_data.db ".tables"
```

### HW 3 Documentation

#### Step 1
Cloned this GitHub repository: https://github.com/hannesrudolph/sqlite-explorer-fastmcp-mcp-server

#### Step 2

Asked Claude Code: I was asked to evaluate the following deployment platforms: AWS, Vercel, 
Railway, and Smithery for my MCP server. I want the simplest and cheapest 
deployment. Which option should I select? 

⏺ Based on your MCP server and requirements, I recommend Smithery.

  Here's why:

  Simplest: Smithery is specifically designed for MCP servers. It has the
  most straightforward deployment process for this exact use case.

  Cheapest: Smithery offers a free tier for MCP server hosting, making it
  the most cost-effective option for your SQLite Explorer MCP server.

  Other options comparison:
  - AWS: Most complex setup, requires managing infrastructure, not
  cost-effective for simple MCP servers
  - Vercel: Designed for web apps/APIs, not optimized for MCP servers,
  serverless model may not fit well
  - Railway: Good platform but more expensive than Smithery's free tier,
  more general-purpose

  For a read-only SQLite MCP server like yours, Smithery's MCP-specific
  infrastructure is the best match for "simplest and cheapest."

#### Step 3

Tested this locally via Cline. In VS Code, we configured the system settings to launch a web-based interface with the following JSON file. See URL: http://localhost:6274/?MCP_PROXY_AUTH_TOKEN=a164e503687338cb23938baf05ae738ebe5cd0eaefa629e419cea7ef6ef51563#tools

#### Step 4
