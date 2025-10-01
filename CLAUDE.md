# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a SQLite Explorer MCP (Model Context Protocol) Server built with the FastMCP framework. It provides safe, read-only access to SQLite databases through MCP tools that can be used by LLMs. The project contains two server implementations and is configured for multiple deployment options.

## Key Commands

### Installation and Setup
```bash
# Install dependencies
pip install -r sqlite-explorer-fastmcp-mcp-server/requirements.txt

# Run local version with environment variable
SQLITE_DB_PATH=/path/to/your/database.db fastmcp run sqlite-explorer-fastmcp-mcp-server/sqlite_explorer_local.py

# Run Smithery deployment version (uses hardcoded path)
fastmcp run sqlite-explorer-fastmcp-mcp-server/sqlite_explorer.py
```

### Testing and Development
```bash
# Test with FastMCP's built-in testing
fastmcp test sqlite-explorer-fastmcp-mcp-server/sqlite_explorer_local.py

# Run with web-based inspector interface
SQLITE_DB_PATH=/path/to/database.db fastmcp dev sqlite-explorer-fastmcp-mcp-server/sqlite_explorer_local.py

# Install for Claude Desktop
SQLITE_DB_PATH=/path/to/database.db fastmcp install sqlite-explorer-fastmcp-mcp-server/sqlite_explorer_local.py --name "SQLite Explorer"

# Add to Claude Desktop configuration
SQLITE_DB_PATH=/path/to/database.db fastmcp claude-desktop add sqlite-explorer-fastmcp-mcp-server/sqlite_explorer_local.py --name "SQLite Explorer"
```

### Deployment Commands
```bash
# Deploy to Smithery platform
SQLITE_DB_PATH=/path/to/database.db smithery playground

# Build Docker container
docker build -t sqlite-explorer sqlite-explorer-fastmcp-mcp-server/
```

## Architecture

### Dual Server Implementation

The project contains two main server files with different deployment strategies:

**sqlite-explorer-fastmcp-mcp-server/sqlite_explorer_local.py** - Local development version:
- Requires `SQLITE_DB_PATH` environment variable
- Uses `fastmcp.FastMCP` import
- Designed for local testing and Claude Desktop integration

**sqlite-explorer-fastmcp-mcp-server/sqlite_explorer.py** - Smithery deployment version:
- Uses hardcoded database path (`financial_data.db` in same directory)
- Uses `mcp.server.fastmcp.FastMCP` import and `@smithery.server()` decorator
- Includes additional type conversions for cloud compatibility (sqlite_explorer.py:163-174)
- Configured for Smithery platform deployment

### Core Components

Both servers implement three identical MCP tools:
- `read_query()` - Execute SELECT queries with comprehensive safety validations
- `list_tables()` - List all database tables
- `describe_table()` - Get detailed table schema information

**SQLiteConnection class** - Context manager for database connections with proper cleanup and row factory configuration

### Safety Features
- Read-only access (only SELECT and WITH queries allowed)
- Query validation and sanitization preventing SQL injection
- Parameter binding support for secure query execution
- Row limit enforcement (default 1000 rows, configurable)
- Multiple statement detection and blocking
- Comprehensive error handling with descriptive messages

### Deployment Configuration

**smithery.yaml** - Smithery platform deployment configuration:
- Container runtime with Dockerfile build
- HTTP start command type
- Server entry point: `sqlite_explorer:create_server`

**pyproject.toml** - Python package configuration:
- FastMCP and Smithery dependencies
- Smithery tool configuration pointing to server creation function
- Hatchling build system

**Dockerfile** - Container deployment:
- Python 3.11 slim base image
- Copies server code and database file
- Module execution entry point

### VSCode/Cline Integration
```json
{
  "sqlite-explorer": {
    "command": "uv",
    "args": [
      "run", "--with", "fastmcp", "--with", "uvicorn", "fastmcp", "run",
      "/path/to/sqlite-explorer-fastmcp-mcp-server/sqlite_explorer_local.py"
    ],
    "env": {
      "SQLITE_DB_PATH": "/path/to/your/database.db"
    }
  }
}
```

## Development Notes

- The `financial_data.db` file is included for testing and demonstration
- Documentation files `mcp-documentation.txt` and `fastmcp-documentation.txt` contain comprehensive framework information
- All database operations use SQLite's row factory for dictionary-style result access
- The server architecture supports both local development and cloud deployment scenarios
- Query validation implements a sophisticated parser to detect multiple statements while handling quoted strings correctly