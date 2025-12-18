# Maya MCP Server

**Connect Claude AI to Autodesk Maya through Model Context Protocol**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Maya 2020+](https://img.shields.io/badge/maya-2020+-green.svg)](https://www.autodesk.com/products/maya/)

[English](README.md) | [简体中文](README_CN.md) | [繁體中文](README_CN_TW.md) | [日本語](README_JP.md) | [한국어](README_KO.md) | [Español](README_ES.md) | [Français](README_FR.md) | [Deutsch](README_DE.md) | [Русский](README_RU.md)

---

## Overview

Maya MCP Server enables Claude AI to directly control Autodesk Maya through the Model Context Protocol, enabling:

- 🎨 AI-assisted 3D modeling
- 🤖 Natural language Maya control
- 📸 Real-time scene preview
- 🔧 Workflow automation

## Quick Start

### 1. Install Dependencies

```bash
pip install "mcp[cli]>=1.3.0"
```

### 2. Load Maya Plugin

Load `plug-ins/maya_mcp.py` in Maya's **Plug-in Manager**:

1. Copy `plug-ins/maya_mcp.py` to:
   - Windows: `C:\Users\<username>\Documents\maya\<version>\plug-ins\`
   - macOS: `~/maya/<version>/plug-ins/`

2. Open Maya → **Windows > Settings/Preferences > Plug-in Manager**

3. Find `maya_mcp.py`, check **Loaded** and **Auto load**

4. Verify in Script Editor:
   ```
   MayaMCP: Plugin loaded successfully
   MayaMCP: Server started at localhost:9877
   ```

### 3. Configure Claude Desktop

Edit config file (**Settings > Developer > Edit Config**):

#### Option A: Using npx (Recommended)

```json
{
  "mcpServers": {
    "maya-mcp": {
      "command": "npx",
      "args": [
        "--yes",
        "--package=YOUR_PROJECT_PATH",
        "maya-mcp"
      ],
      "env": {
        "MAYA_HOST": "localhost",
        "MAYA_PORT": "9877"
      }
    }
  }
}
```

#### Option B: Using Python

```json
{
  "mcpServers": {
    "maya-mcp": {
      "command": "python",
      "args": ["-m", "maya_mcp.server"],
      "env": {
        "PYTHONPATH": "YOUR_PROJECT_PATH/src",
        "MAYA_HOST": "localhost",
        "MAYA_PORT": "9877"
      }
    }
  }
}
```

> 💡 More configuration options in [`examples/`](examples/)

### 4. Test Connection

Restart Claude Desktop, then ask:

```
Get current Maya scene information
```

If you see scene info returned, it's working! ✅

## Features

### 🛠️ Core Tools

| Tool | Function |
|------|----------|
| `get_scene_info` | Get scene information (objects, cameras, lights) |
| `get_object_info` | Get object details (position, rotation, material) |
| `create_primitive` | Create geometry (cube/sphere/cylinder/plane/torus) |
| `delete_object` | Delete objects |
| `transform_object` | Transform objects (move/rotate/scale) |
| `set_material` | Set materials and colors |
| `execute_maya_code` | Execute Python code |
| `get_viewport_screenshot` | Capture viewport screenshot ⚠️ |
| `smart_select` | Smart object selection with regex and filters |
| `get_scene_summary` | Get comprehensive scene summary |
| `get_console_output` | Get Maya console/script editor output 🆕 |

> ⚠️ Note: `get_viewport_screenshot` may be unstable in some Maya versions due to playblast compatibility issues.

### 💬 Example Conversations

```
User: Create a red cube at position (0, 5, 0)

Claude: 
1. Created cube
2. Moved to specified position
3. Applied red material
✅ Done
```

```
User: Create a simple table and chair scene and capture a screenshot

Claude:
1. Created table top (scaled cube)
2. Created 4 table legs (cylinders)
3. Created chair
4. Set materials
5. Captured viewport screenshot
✅ [Shows screenshot]
```

## Usage Examples

### Basic Operations

```
# Scene queries
"Show all objects in the current scene"
"Get detailed info for pCube1"
"Get console output to see recent Maya logs"

# Create objects
"Create a sphere named mySphere"
"Create 10 cubes in a row"

# Modify objects
"Move pCube1 to (5, 0, 0)"
"Set pSphere1 to blue"
"Rotate pCylinder1 45 degrees on Y axis"

# Smart selection
"Select all objects with 'character' in their name"
"Find all meshes with more than 5000 faces"
```

### Advanced Operations

```
# Procedural modeling
"Execute code to create a 5x5 cube grid"

# Vertex/Face editing
"Create a plane and edit vertices to make a terrain"
"Extrude faces to create details"

# UV editing
"Apply automatic UV projection to selected objects"
"Create spherical UV mapping for the sphere"

# Animation
"Create keyframe animation for bouncing ball"
"Set up 3-point lighting system"

# Rigging
"Create a spine bone chain with 5 joints"
"Set up parent constraints"

# Dynamics
"Create particle system with gravity"
"Apply bend deformer to plane"

# Boolean operations
"Subtract cube2 from cube1"
"Union two overlapping spheres"

# Batch operations
"Set all spheres to random colors"

# Complex scenes
"Create a simple interior scene with floor, walls, and furniture"
```

## Configuration Options

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MAYA_HOST` | `localhost` | Maya server address |
| `MAYA_PORT` | `9877` | Maya server port |
| `PYTHONPATH` | - | Python module search path (Python direct mode only) |

### Custom Port

**In Maya plugin:**
```python
start_maya_mcp_server(host='localhost', port=9878)
```

**In config file:**
```json
"env": {
  "MAYA_PORT": "9878"
}
```

## Troubleshooting

### Connection Failed

**Issue:** "Cannot connect to Maya"

**Solutions:**
1. ✅ Verify Maya is running
2. ✅ Confirm plugin is loaded (check Plug-in Manager)
3. ✅ Check Script Editor for startup messages
4. ✅ Ensure port 9877 is not in use

### Module Not Found

**Issue:** "ModuleNotFoundError: No module named 'maya_mcp'"

**Solutions:**
1. Install dependencies: `pip install "mcp[cli]>=1.3.0"`
2. Check PYTHONPATH setting (if using Python direct mode)
3. Try using npx method instead

### Plugin Load Failed

**Issue:** Maya reports "No initializePlugin() function"

**Solutions:**
- Ensure using latest version of `maya_mcp.py`
- Plugin file contains `initializePlugin()` and `uninitializePlugin()` functions

## Security Notes

⚠️ **Important:**

- `execute_maya_code` tool allows execution of arbitrary Python code
- Always **save Maya scene** before executing
- Use with caution in production environments
- Test operations in a test scene first

## Logs

Server logs are saved at:
- **Windows:** `%TEMP%\maya-mcp\maya-mcp.log`
- **macOS/Linux:** `/tmp/maya-mcp/maya-mcp.log`

Check logs to debug connection issues or command execution errors.

## Development

### Adding New Tools

1. Add command handler in `plug-ins/maya_mcp.py`
2. Add MCP tool definition in `src/maya_mcp/server.py`
3. Test new tool

### Run Development Server

```bash
# Set environment
export PYTHONPATH=/path/to/maya-mcp-server/src

# Run server
python -m maya_mcp.server
```

## Contributing

Contributions welcome! See [`CONTRIBUTING.md`](CONTRIBUTING.md)

## Acknowledgments

Inspired by:
- [Blender-MCP](https://github.com/ahujasid/blender-mcp) - Architecture reference

## License

[MIT License](LICENSE)

## Disclaimer

This is a third-party project, not an official Autodesk product.

---

<div align="center">

**[Get Started](examples/)** • **[Configuration Guide](examples/README.md)** • **[Report Issues](../../issues)**

Made with ❤️ for Maya artists and AI enthusiasts

</div>