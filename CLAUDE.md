# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a SQLite Explorer MCP (Model Context Protocol) Server built with the FastMCP framework. It provides safe, read-only access to SQLite databases through MCP tools that can be used by LLMs.

## Key Commands

### Installation and Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Install for Claude Desktop
fastmcp install sqlite_explorer.py --name "SQLite Explorer" -e SQLITE_DB_PATH=/path/to/db

# Run the server directly
fastmcp run sqlite_explorer.py
```

### Testing the Server
```bash
# Test with FastMCP's built-in testing
fastmcp test sqlite_explorer.py

# Run with environment variable
SQLITE_DB_PATH=/path/to/your/database.db fastmcp run sqlite_explorer.py
```

## Architecture

### Core Components

**sqlite_explorer.py:164** - Main MCP server implementation with three key tools:
- `read_query()` - Execute SELECT queries with safety validations
- `list_tables()` - List all database tables
- `describe_table()` - Get table schema information

**SQLiteConnection class:16-28** - Context manager for database connections with proper cleanup

### Safety Features
- Read-only access (only SELECT and WITH queries allowed)
- Query validation and sanitization
- Parameter binding support
- Row limit enforcement (default 1000 rows)
- Multiple statement detection and blocking

### Environment Configuration
- `SQLITE_DB_PATH` - Required environment variable pointing to the SQLite database file
- Server uses log level "CRITICAL" to suppress progress output

## MCP Integration

This server follows the FastMCP framework patterns:
- Uses `@mcp.tool()` decorators to expose functions as MCP tools
- Implements proper error handling with descriptive messages
- Returns structured data as lists and dictionaries
- Integrates with Claude Desktop and Cline VSCode plugin

## Development Notes

- The codebase includes comprehensive documentation in `mcp-documentation.txt` and `fastmcp-documentation.txt`
- All database operations use SQLite's row factory for dictionary-style access
- Query validation prevents SQL injection and ensures read-only access
- The server is designed to be deployed as an MCP tool for LLM interactions