"""Maya integration through the Model Context Protocol."""

__version__ = "1.3.8"

# Don't import from server here to avoid circular import issues
# Users can import directly: from maya_mcp.server import MayaConnection