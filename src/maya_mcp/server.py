"""
Maya MCP Server
Implements the Model Context Protocol for Maya integration
"""

from mcp.server.fastmcp import FastMCP, Context, Image
import socket
import json
import asyncio
import logging
import tempfile
from dataclasses import dataclass, field
from contextlib import asynccontextmanager
from typing import AsyncIterator, Dict, Any
import os
from pathlib import Path
import base64
import time
import threading

# Configure logs - output to a file to avoid interfering with MCP's stdio communication
log_dir = os.path.join(tempfile.gettempdir(), 'maya-mcp')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'maya-mcp.log')

# Create file handler
file_handler = logging.FileHandler(log_file, encoding='utf-8')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

# Configure logger (don't use basicConfig to avoid output to stderr)
logger = logging.getLogger("MayaMCPServer")
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.propagate = False  # Prevent propagation to root logger

# Log file location to stderr (only at startup)
import sys
print(f"Maya MCP log file: {log_file}", file=sys.stderr)

# Default configuration
DEFAULT_HOST = "localhost"
DEFAULT_PORT = 9877

@dataclass
class MayaConnection:
    """Maya connection management (with connection pooling and retry mechanism)"""
    host: str
    port: int
    sock: socket.socket = None
    last_used: float = 0
    connection_count: int = 0
    max_idle_time: float = 300.0  # 5 minute idle timeout
    
    def connect(self, retry_count: int = 3, retry_delay: float = 1.0) -> bool:
        """Connect to Maya plugin socket server (with retry mechanism)"""
        if self.sock:
            # Check if connection is still valid
            try:
                self.sock.settimeout(1.0)
                # Try sending empty bytes to test connection
                self.sock.send(b'')
                return True
            except:
                # Connection is broken, close and reconnect
                self.disconnect()
        
        last_error = None
        for attempt in range(retry_count):
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                self.sock.settimeout(10.0)  # 10 second connection timeout
                self.sock.connect((self.host, self.port))
                self.connection_count += 1
                self.last_used = time.time()
                logger.info(f"Connected to Maya: {self.host}:{self.port} (attempt {attempt + 1}/{retry_count})")
                return True
            except Exception as e:
                last_error = e
                logger.warning(f"Failed to connect to Maya (attempt {attempt + 1}/{retry_count}): {str(e)}")
                self.sock = None
                if attempt < retry_count - 1:
                    time.sleep(retry_delay)
        
        logger.error(f"Failed to connect to Maya after {retry_count} attempts: {str(last_error)}")
        return False
    
    def disconnect(self):
        """Disconnect from Maya"""
        if self.sock:
            try:
                self.sock.shutdown(socket.SHUT_RDWR)
            except:
                pass
            try:
                self.sock.close()
            except Exception as e:
                logger.error(f"Error disconnecting from Maya: {str(e)}")
            finally:
                self.sock = None
                logger.info("Disconnected from Maya")
    
    def is_idle_too_long(self) -> bool:
        """Check if connection has been idle too long"""
        if self.last_used == 0:
            return False
        return (time.time() - self.last_used) > self.max_idle_time
    
    def receive_full_response(self, sock, buffer_size=8192, timeout=180.0):
        """Receive complete response, supporting large data and timeout control"""
        chunks = []
        sock.settimeout(timeout)
        total_size = 0
        max_size = 100 * 1024 * 1024  # 100MB max response size
        start_time = time.time()
        
        try:
            while True:
                try:
                    # Check timeout
                    elapsed = time.time() - start_time
                    if elapsed > timeout:
                        raise socket.timeout("Receive timeout")
                    
                    chunk = sock.recv(buffer_size)
                    if not chunk:
                        if not chunks:
                            raise Exception("Connection closed before receiving any data")
                        break
                    
                    chunks.append(chunk)
                    total_size += len(chunk)
                    
                    # Prevent memory overflow
                    if total_size > max_size:
                        raise Exception(f"Response too large (>{max_size} bytes), possible memory overflow")
                    
                    # Log progress every 10MB received
                    if total_size % (10 * 1024 * 1024) < buffer_size:
                        logger.info(f"Receiving large data... ({total_size / (1024*1024):.1f} MB)")
                    
                    # Check if complete JSON object has been received
                    try:
                        data = b''.join(chunks)
                        json.loads(data.decode('utf-8'))
                        elapsed = time.time() - start_time
                        logger.info(f"Received complete response ({total_size} bytes, took {elapsed:.2f}s)")
                        return data
                    except json.JSONDecodeError:
                        # JSON incomplete, continue receiving
                        continue
                    except UnicodeDecodeError as e:
                        logger.error(f"Decode error: {str(e)}")
                        raise Exception("Response contains invalid UTF-8 characters")
                        
                except socket.timeout:
                    elapsed = time.time() - start_time
                    logger.warning(f"Socket timeout during receive (received {total_size} bytes, took {elapsed:.2f}s)")
                    break
                except (ConnectionError, BrokenPipeError, ConnectionResetError) as e:
                    logger.error(f"Socket connection error during receive: {str(e)}")
                    raise
                    
        except socket.timeout:
            elapsed = time.time() - start_time
            logger.warning(f"Timeout during receive (received {total_size} bytes, took {elapsed:.2f}s)")
        except Exception as e:
            logger.error(f"Error during receive: {str(e)}")
            raise
            
        # Try using received data
        if chunks:
            data = b''.join(chunks)
            logger.info(f"Returning data after receive completion ({total_size} bytes)")
            try:
                json.loads(data.decode('utf-8'))
                return data
            except json.JSONDecodeError:
                raise Exception(f"Received incomplete JSON response (received {total_size} bytes)")
            except UnicodeDecodeError:
                raise Exception("Response contains invalid UTF-8 characters")
        else:
            raise Exception("No data received")
    
    def send_command(self, command_type: str, params: Dict[str, Any] = None, timeout: float = 180.0) -> Dict[str, Any]:
        """Send command to Maya and return response (with retry and performance monitoring)"""
        start_time = time.time()
        
        # Check idle timeout
        if self.is_idle_too_long():
            logger.info("Connection idle too long, reconnecting")
            self.disconnect()
        
        if not self.sock and not self.connect():
            raise ConnectionError("Not connected to Maya")
        
        command = {
            "type": command_type,
            "params": params or {}
        }
        
        # Check command size
        command_json = json.dumps(command, ensure_ascii=False)
        command_size = len(command_json.encode('utf-8'))
        if command_size > 10 * 1024 * 1024:  # 10MB
            raise Exception(f"Command too large ({command_size} bytes), exceeds 10MB limit")
        
        retry_count = 2
        last_error = None
        
        for attempt in range(retry_count):
            try:
                # Log command being sent
                logger.info(f"Sending command (attempt {attempt + 1}/{retry_count}): {command_type}")
                if params:
                    logger.debug(f"Parameters: {params}")
                
                # Send command
                self.sock.sendall(command_json.encode('utf-8'))
                self.last_used = time.time()
                logger.info(f"Command sent ({command_size} bytes), waiting for response...")
                
                # Set receive timeout
                self.sock.settimeout(timeout)
                
                # Receive response
                response_data = self.receive_full_response(self.sock, timeout=timeout)
                logger.info(f"Received {len(response_data)} bytes of data")
                
                response = json.loads(response_data.decode('utf-8'))
                
                # Log execution time
                execution_time = time.time() - start_time
                logger.info(f"Command '{command_type}' completed, status: {response.get('status', 'unknown')}, total time: {execution_time:.2f}s")
                
                if execution_time > 60:
                    logger.warning(f"Command execution time is long: {execution_time:.2f}s")
                
                if response.get("status") == "error":
                    error_msg = response.get('message', 'Maya returned unknown error')
                    logger.error(f"Maya error: {error_msg}")
                    raise Exception(error_msg)
                
                self.last_used = time.time()
                return response.get("result", {})
                
            except socket.timeout:
                last_error = "Waiting for Maya response timeout"
                logger.error(f"{last_error} (attempt {attempt + 1}/{retry_count})")
                self.disconnect()
                if attempt < retry_count - 1:
                    logger.info("Retrying...")
                    time.sleep(1.0)
                    if not self.connect():
                        break
                    
            except (ConnectionError, BrokenPipeError, ConnectionResetError) as e:
                last_error = f"Lost connection to Maya: {str(e)}"
                logger.error(f"{last_error} (attempt {attempt + 1}/{retry_count})")
                self.disconnect()
                if attempt < retry_count - 1:
                    logger.info("Retrying...")
                    time.sleep(1.0)
                    if not self.connect():
                        break
                        
            except json.JSONDecodeError as e:
                last_error = f"Maya returned invalid response: {str(e)}"
                logger.error(last_error)
                if 'response_data' in locals() and response_data:
                    logger.error(f"Raw response (first 500 bytes): {response_data[:500]}")
                self.disconnect()
                break  # Don't retry JSON errors
                
            except Exception as e:
                last_error = f"Error communicating with Maya: {str(e)}"
                logger.error(f"{last_error} (attempt {attempt + 1}/{retry_count})")
                self.disconnect()
                if attempt < retry_count - 1:
                    logger.info("Retrying...")
                    time.sleep(1.0)
                    if not self.connect():
                        break
        
        # All retries failed
        raise Exception(last_error or "Failed to communicate with Maya")

@asynccontextmanager
async def server_lifespan(server: FastMCP) -> AsyncIterator[Dict[str, Any]]:
    """Manage server startup and shutdown lifecycle"""
    try:
        logger.info("MayaMCP server starting")
        
        # Try connecting to Maya at startup to verify availability
        try:
            maya = get_maya_connection()
            logger.info("Successfully connected to Maya at startup")
        except Exception as e:
            logger.warning(f"Unable to connect to Maya at startup: {str(e)}")
            logger.warning("Please ensure Maya plugin is running before using Maya resources or tools")
        
        yield {}
    finally:
        # Clean up global connection on shutdown
        global _maya_connection
        if _maya_connection:
            logger.info("Disconnecting from Maya on shutdown")
            _maya_connection.disconnect()
            _maya_connection = None
        logger.info("MayaMCP server shut down")

# Create MCP server with lifecycle support
mcp = FastMCP(
    "MayaMCP",
    lifespan=server_lifespan
)

# Global connection for resources (since resources can't access context)
_maya_connection = None
_connection_lock = threading.Lock()

def get_maya_connection():
    """Get or create persistent Maya connection (thread-safe)"""
    global _maya_connection
    
    with _connection_lock:
        # If existing connection exists, check if it's still valid
        if _maya_connection is not None:
            # Check idle timeout
            if _maya_connection.is_idle_too_long():
                logger.info("Connection idle too long, closing and recreating")
                try:
                    _maya_connection.disconnect()
                except:
                    pass
                _maya_connection = None
            else:
                # Quick connection validation
                try:
                    if _maya_connection.sock:
                        return _maya_connection
                except:
                    pass
        
        # Create new connection if needed
        if _maya_connection is None:
            host = os.getenv("MAYA_HOST", DEFAULT_HOST)
            port = int(os.getenv("MAYA_PORT", DEFAULT_PORT))
            _maya_connection = MayaConnection(host=host, port=port)
            if not _maya_connection.connect():
                logger.error("Failed to connect to Maya")
                _maya_connection = None
                raise Exception("Unable to connect to Maya. Please ensure Maya plugin is running.")
            logger.info(f"Created new persistent connection to Maya (connection count: {_maya_connection.connection_count})")
        
        return _maya_connection

# ==================== MCP Tool Definitions ====================

@mcp.tool()
def get_scene_info(ctx: Context) -> str:
    """Get detailed information about the current Maya scene"""
    try:
        maya = get_maya_connection()
        result = maya.send_command("get_scene_info")
        return json.dumps(result, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Error getting scene info from Maya: {str(e)}")
        return f"Error getting scene info: {str(e)}"

@mcp.tool()
def get_object_info(ctx: Context, object_name: str) -> str:
    """
    Get detailed information about a specific object in the Maya scene.
    
    Parameters:
    - object_name: Name of the object to get information for
    """
    try:
        maya = get_maya_connection()
        result = maya.send_command("get_object_info", {"name": object_name})
        return json.dumps(result, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Error getting object info from Maya: {str(e)}")
        return f"Error getting object info: {str(e)}"

@mcp.tool()
def execute_maya_code(ctx: Context, code: str) -> str:
    """
    Execute arbitrary Python code in Maya. Ensure step-by-step execution by breaking it into smaller chunks.
    
    Parameters:
    - code: Python code to execute
    
    Note: This tool has safety limits to prevent Maya crashes:
    - Max code length: 50KB
    - Execution timeout: 3 minutes
    - Restricted dangerous operations (e.g., file system access)
    """
    try:
        # Additional client-side validation
        if len(code) > 50000:
            return f"Error: Code too long ({len(code)} characters), maximum 50000 characters allowed"
        
        maya = get_maya_connection()
        result = maya.send_command("execute_code", {"code": code}, timeout=180.0)
        
        output = result.get('output', '')
        exec_time = result.get('execution_time', 'N/A')
        return f"Code executed successfully (took: {exec_time}):\n{output}"
    except Exception as e:
        logger.error(f"Error executing code: {str(e)}")
        return f"Error executing code: {str(e)}"

@mcp.tool()
def create_primitive(
    ctx: Context,
    prim_type: str,
    name: str = None,
    translation: list = None,
    rotation: list = None,
    scale: list = None
) -> str:
    """
    Create basic geometry in Maya.
    
    Parameters:
    - prim_type: Geometry type (cube, sphere, cylinder, plane, torus)
    - name: Optional object name
    - translation: Optional position [x, y, z]
    - rotation: Optional rotation [x, y, z] (degrees)
    - scale: Optional scale [x, y, z]
    """
    try:
        maya = get_maya_connection()
        params = {"type": prim_type}
        if name:
            params["name"] = name
        if translation:
            params["translation"] = translation
        if rotation:
            params["rotation"] = rotation
        if scale:
            params["scale"] = scale
            
        result = maya.send_command("create_primitive", params)
        return f"Geometry created successfully: {result.get('object', '')}"
    except Exception as e:
        logger.error(f"Error creating geometry: {str(e)}")
        return f"Error creating geometry: {str(e)}"

@mcp.tool()
def delete_object(ctx: Context, object_name: str) -> str:
    """
    Delete an object from the Maya scene.
    
    Parameters:
    - object_name: Name of the object to delete
    """
    try:
        maya = get_maya_connection()
        result = maya.send_command("delete_object", {"name": object_name})
        return result.get("message", "Object deleted")
    except Exception as e:
        logger.error(f"Error deleting object: {str(e)}")
        return f"Error deleting object: {str(e)}"

@mcp.tool()
def set_material(
    ctx: Context,
    object_name: str,
    color: list = None,
    material_name: str = None
) -> str:
    """
    Set material and color for a Maya object.
    
    Parameters:
    - object_name: Name of the object to apply material to
    - color: RGB color values [r, g, b] (0-1 range)
    - material_name: Optional material name
    """
    try:
        maya = get_maya_connection()
        params = {"object": object_name}
        if color:
            params["color"] = color
        if material_name:
            params["material_name"] = material_name
            
        result = maya.send_command("set_material", params)
        return f"Material applied: {result.get('material', '')}"
    except Exception as e:
        logger.error(f"Error setting material: {str(e)}")
        return f"Error setting material: {str(e)}"

@mcp.tool()
def transform_object(
    ctx: Context,
    object_name: str,
    translation: list = None,
    rotation: list = None,
    scale: list = None
) -> str:
    """
    Transform a Maya object (move, rotate, scale) with parameter validation.
    
    Parameters:
    - object_name: Name of the object to transform
    - translation: New position [x, y, z] (validated range: -1e6 to 1e6)
    - rotation: New rotation [x, y, z] in degrees (validated range: -360000 to 360000)
    - scale: New scale [x, y, z] (validated range: 0.0001 to 10000, must be > 0)
    
    All operations are wrapped in undo chunks for safety.
    If operation fails, changes are automatically undone.
    """
    try:
        # Client-side parameter validation
        def validate_vector(vec, name, min_val, max_val):
            if vec is not None:
                if not isinstance(vec, (list, tuple)) or len(vec) != 3:
                    raise ValueError(f"{name} must be a list of 3 numbers")
                for i, val in enumerate(vec):
                    if not isinstance(val, (int, float)):
                        raise ValueError(f"{name}[{i}] must be a number")
                    if val < min_val or val > max_val:
                        raise ValueError(f"{name}[{i}] value {val} out of range [{min_val}, {max_val}]")
        
        # Validate parameters
        if translation:
            validate_vector(translation, "translation", -1e6, 1e6)
        if rotation:
            validate_vector(rotation, "rotation", -360000, 360000)
        if scale:
            validate_vector(scale, "scale", 0.0001, 10000)
        
        maya = get_maya_connection()
        params = {"object": object_name}
        if translation:
            params["translation"] = translation
        if rotation:
            params["rotation"] = rotation
        if scale:
            params["scale"] = scale
            
        result = maya.send_command("transform_object", params)
        return result.get("message", "Object transformed") + " (Undo available)"
    except ValueError as ve:
        logger.error(f"Parameter validation error: {str(ve)}")
        return f"Parameter validation error: {str(ve)}"
    except Exception as e:
        logger.error(f"Error transforming object: {str(e)}")
        return f"Error transforming object: {str(e)}"

@mcp.tool()
def get_viewport_screenshot(ctx: Context, max_size: int = 800) -> Image:
    """
    Capture a screenshot of the current Maya 3D viewport.
    
    Parameters:
    - max_size: Maximum size in pixels (default: 800)
    
    Returns screenshot as an image.
    
    Note: Screenshot operation has a 60 second timeout limit.
    """
    try:
        maya = get_maya_connection()
        
        # Create temporary file path
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, f"maya_screenshot_{os.getpid()}_{int(time.time())}.jpg")
        
        # Use shorter timeout to prevent long waits
        result = maya.send_command("get_viewport_screenshot", {
            "filepath": temp_path
        }, timeout=60.0)
        
        if "error" in result:
            raise Exception(result["error"])
        
        # Get actual file path (Maya may return a different path)
        actual_path = result.get("filepath", temp_path)
        
        if not os.path.exists(actual_path):
            raise Exception(f"Screenshot file was not created: {actual_path}")
        
        # Check file size
        file_size = os.path.getsize(actual_path)
        if file_size > 10 * 1024 * 1024:  # 10MB
            logger.warning(f"Screenshot file is large: {file_size / (1024*1024):.1f}MB")
        
        # Read file
        with open(actual_path, 'rb') as f:
            image_bytes = f.read()
        
        logger.info(f"Screenshot successful, size: {len(image_bytes)} bytes")
        
        # Delete temporary file
        try:
            os.remove(actual_path)
        except Exception as cleanup_error:
            logger.warning(f"Failed to cleanup temporary file: {str(cleanup_error)}")
        
        return Image(data=image_bytes, format="jpeg")
        
    except Exception as e:
        logger.error(f"Error capturing screenshot: {str(e)}")
        raise Exception(f"Screenshot failed: {str(e)}")

@mcp.tool()
def smart_select(
    ctx: Context,
    query: str = "",
    type: str = "all",
    attribute_filter: dict = None
) -> str:
    """
    Smart selection of objects based on patterns and attributes.
    
    Parameters:
    - query: Regular expression pattern to match object names (default: "")
    - type: Object type to filter (all, mesh, transform, camera, light, etc.)
    - attribute_filter: Dictionary of attribute filters, e.g. {"faces": ">5000"}
    
    Returns objects with UUID to avoid name conflicts.
    
    Examples:
    - Find all meshes with more than 5000 faces: type="mesh", attribute_filter={"faces": ">5000"}
    - Find all objects with "cube" in name: query="cube"
    - Find all transform nodes: type="transform"
    """
    try:
        maya = get_maya_connection()
        params = {
            "query": query,
            "type": type
        }
        if attribute_filter:
            params["attribute_filter"] = attribute_filter
            
        result = maya.send_command("smart_select", params)
        return json.dumps(result, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Error in smart select: {str(e)}")
        return f"Error in smart select: {str(e)}"

@mcp.tool()
def get_scene_summary(ctx: Context) -> str:
    """
    Get a comprehensive summary of the Maya scene.
    
    Returns hierarchy tree, material list, total vertex/face count,
    providing AI with a global view of the scene.
    """
    try:
        maya = get_maya_connection()
        
        # Get basic scene info
        scene_info = maya.send_command("get_scene_info")
        
        # Add summary statistics
        summary = {
            "scene_info": scene_info,
            "summary": {
                "total_objects": scene_info.get("total_objects", 0),
                "transforms": scene_info.get("transforms", 0),
                "cameras": scene_info.get("cameras", 0),
                "lights": scene_info.get("lights", 0),
                "materials": scene_info.get("materials", 0)
            },
            "selection": scene_info.get("selection", []),
            "timeline": {
                "current_time": scene_info.get("current_time", 1),
                "fps": scene_info.get("fps", 24)
            }
        }
        
        return json.dumps(summary, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Error getting scene summary: {str(e)}")
        return f"Error getting scene summary: {str(e)}"

@mcp.prompt()
def maya_workflow_tips() -> str:
    """Provide Maya workflow tips and best practices"""
    return """
# Maya MCP Workflow Tips

## Basic Operation Flow

1. **Scene Exploration**
   - Use `get_scene_info` to understand current scene
   - Use `get_object_info` to check specific objects

2. **Creating Objects**
   - Use `create_primitive` to create basic geometry
   - Supported types: cube, sphere, cylinder, plane, torus

3. **Modifying Objects**
   - Use `transform_object` to move, rotate, scale
   - Use `set_material` to apply colors and materials

4. **Advanced Operations**
   - Use `execute_maya_code` to execute complex Maya commands
   - Use `get_viewport_screenshot` to visualize results

## Best Practices

- Check scene state before executing complex operations
- Execute complex tasks step by step
- Use screenshots to verify results
- Keep object naming clear and meaningful

## Safety Tips

- `execute_maya_code` is powerful but use with caution
- Always save your work before executing
- Test code with simple scenes
"""

def main():
    """Entry point for the MCP server"""
    import sys
    
    # Log startup
    logger.info("Starting MayaMCP server...")
    
    try:
        # Run server
        mcp.run()
    except KeyboardInterrupt:
        logger.info("Received interrupt signal, shutting down...")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()