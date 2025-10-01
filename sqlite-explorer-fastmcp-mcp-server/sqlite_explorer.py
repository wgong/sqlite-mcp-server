from pathlib import Path
import sqlite3
import os
import logging
from typing import List, Dict, Any, Optional
from fastmcp import FastMCP
from pydantic import BaseModel, Field
from smithery.decorators import smithery

# Configure logging for better debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# For Smithery, need create_server function, within which we have our tools
@smithery.server()
def create_server():
    """Create and configure the SQLite Explorer MCP server."""

    try:
        # Get database path - hardcoded to financial_data.db in same folder
        db_path = Path(__file__).parent / "financial_data.db"
        DB_PATH = db_path

        # Verify database exists
        if not DB_PATH.exists():
            logger.error(f"Database file not found at: {DB_PATH}")
            raise FileNotFoundError(f"Database file not found at: {DB_PATH}")

        logger.info(f"Initializing SQLite Explorer with database: {DB_PATH}")

        # Create FastMCP server without deprecated log_level parameter
        mcp = FastMCP("SQLite Explorer")

        # Configure CORS for cross-origin requests (if needed)
        logger.info("Configuring server for HTTP access")

        # Note: FastMCP/Smithery typically handles CORS automatically
        # If manual CORS configuration is needed, it would be done at the
        # Starlette/FastAPI app level, not in the MCP server code

        class SQLiteConnection:
            def __init__(self, db_path: Path):
                self.db_path = db_path
                self.conn = None

            def __enter__(self):
                self.conn = sqlite3.connect(str(self.db_path))
                self.conn.row_factory = sqlite3.Row
                return self.conn

            def __exit__(self, exc_type, exc_val, exc_tb):
                if self.conn:
                    self.conn.close()

        @mcp.tool()
        def read_query(
            query: str,
            params: Optional[List[Any]] = None,
            fetch_all: bool = True,
            row_limit: int = 1000
        ) -> List[Dict[str, Any]]:
            """Execute a query on the SQLite database.

            Args:
                query: SELECT SQL query to execute
                params: Optional list of parameters for the query
                fetch_all: If True, fetches all results. If False, fetches one row.
                row_limit: Maximum number of rows to return (default 1000)

            Returns:
                List of dictionaries containing the query results
            """
            if not DB_PATH.exists():
                raise FileNotFoundError(f"SQLite database not found at: {DB_PATH}")

            # Clean and validate the query
            query = query.strip()

            # Remove trailing semicolon if present
            if query.endswith(';'):
                query = query[:-1].strip()

            # Check for multiple statements by looking for semicolons not inside quotes
            def contains_multiple_statements(sql: str) -> bool:
                in_single_quote = False
                in_double_quote = False
                for char in sql:
                    if char == "'" and not in_double_quote:
                        in_single_quote = not in_single_quote
                    elif char == '"' and not in_single_quote:
                        in_double_quote = not in_double_quote
                    elif char == ';' and not in_single_quote and not in_double_quote:
                        return True
                return False

            if contains_multiple_statements(query):
                raise ValueError("Multiple SQL statements are not allowed")

            # Validate query type (allowing common CTEs)
            query_lower = query.lower()
            if not any(query_lower.startswith(prefix) for prefix in ('select', 'with')):
                raise ValueError("Only SELECT queries (including WITH clauses) are allowed for safety")

            params = params or []

            with SQLiteConnection(DB_PATH) as conn:
                cursor = conn.cursor()

                try:
                    # Only add LIMIT if query doesn't already have one
                    if 'limit' not in query_lower:
                        query = f"{query} LIMIT {row_limit}"

                    cursor.execute(query, params)

                    if fetch_all:
                        results = cursor.fetchall()
                    else:
                        results = [cursor.fetchone()]

                    return [dict(row) for row in results if row is not None]

                except sqlite3.Error as e:
                    raise ValueError(f"SQLite error: {str(e)}")

        @mcp.tool()
        def list_tables() -> List[str]:
            """List all tables in the SQLite database.

            Returns:
                List of table names in the database
            """
            if not DB_PATH.exists():
                raise FileNotFoundError(f"SQLite database not found at: {DB_PATH}")

            with SQLiteConnection(DB_PATH) as conn:
                cursor = conn.cursor()

                try:
                    cursor.execute("""
                        SELECT name FROM sqlite_master
                        WHERE type='table'
                        ORDER BY name
                    """)

                    return [row['name'] for row in cursor.fetchall()]

                except sqlite3.Error as e:
                    raise ValueError(f"SQLite error: {str(e)}")

        @mcp.tool()
        def describe_table(table_name: str) -> List[Dict[str, str]]:
            """Get detailed information about a table's schema.

            Args:
                table_name: Name of the table to describe

            Returns:
                List of dictionaries containing column information:
                - name: Column name
                - type: Column data type
                - notnull: Whether the column can contain NULL values
                - dflt_value: Default value for the column
                - pk: Whether the column is part of the primary key
            """
            if not DB_PATH.exists():
                raise FileNotFoundError(f"SQLite database not found at: {DB_PATH}")

            with SQLiteConnection(DB_PATH) as conn:
                cursor = conn.cursor()

                try:
                    # Verify table exists
                    cursor.execute("""
                        SELECT name FROM sqlite_master
                        WHERE type='table' AND name=?
                    """, [table_name])

                    if not cursor.fetchone():
                        raise ValueError(f"Table '{table_name}' does not exist")

                    # Get table schema
                    cursor.execute(f"PRAGMA table_info({table_name})")
                    columns = cursor.fetchall()

                    # Convert all values to strings for compatibility
                    result = []
                    for row in columns:
                        row_dict = dict(row)
                        # Convert integers and None to strings
                        for key, value in row_dict.items():
                            if value is None:
                                row_dict[key] = ""
                            else:
                                row_dict[key] = str(value)
                        result.append(row_dict)

                    return result

                except sqlite3.Error as e:
                    raise ValueError(f"SQLite error: {str(e)}")

        # Add a simple health check tool
        @mcp.tool()
        def health_check() -> Dict[str, str]:
            """Check if the server and database are working properly."""
            try:
                with SQLiteConnection(DB_PATH) as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT 1 as test")
                    result = cursor.fetchone()
                    if result and result[0] == 1:
                        return {
                            "status": "healthy",
                            "database": str(DB_PATH),
                            "message": "SQLite Explorer server is running properly"
                        }
                    else:
                        return {
                            "status": "error",
                            "database": str(DB_PATH),
                            "message": "Database test query failed"
                        }
            except Exception as e:
                return {
                    "status": "error",
                    "database": str(DB_PATH),
                    "message": f"Health check failed: {str(e)}"
                }

        logger.info("SQLite Explorer MCP server initialized successfully")
        logger.info(f"Available tools: read_query, list_tables, describe_table, health_check")

        return mcp

    except Exception as e:
        logger.error(f"Failed to create server: {str(e)}")
        raise