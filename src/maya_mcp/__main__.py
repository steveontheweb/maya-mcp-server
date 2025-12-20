"""
Entry point for running maya_mcp as a module.
Supports: python -m maya_mcp.server
"""

from .server import main

if __name__ == "__main__":
    main()