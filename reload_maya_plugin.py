"""
Maya Plugin Force Reload Script
Run this script in Maya's Script Editor to force reload the plugin
"""

import maya.cmds as cmds
import sys
import os

def force_reload_plugin():
    """Force reload the Maya MCP plugin with complete cache clearing"""
    
    plugin_path = "D:/Documents/maya/plug-ins/maya_mcp.py"
    plugin_name = "maya_mcp.py"
    
    print("=" * 60)
    print("Force Reloading Maya MCP Plugin")
    print("=" * 60)
    
    # Step 1: Unload plugin
    print("\n1. Unloading plugin...")
    try:
        if cmds.pluginInfo(plugin_name, query=True, loaded=True):
            cmds.unloadPlugin(plugin_name, force=True)
            print("   Plugin unloaded successfully")
        else:
            print("   Plugin was not loaded")
    except:
        print("   Warning: Could not unload plugin")
    
    # Step 2: Clear Python module cache
    print("\n2. Clearing Python module cache...")
    modules_to_clear = []
    for module_name in list(sys.modules.keys()):
        if 'maya_mcp' in module_name.lower():
            modules_to_clear.append(module_name)
    
    for module_name in modules_to_clear:
        print(f"   Removing module: {module_name}")
        del sys.modules[module_name]
    
    # Step 3: Clear .pyc files
    print("\n3. Clearing .pyc cache files...")
    plugin_dir = os.path.dirname(plugin_path)
    for root, dirs, files in os.walk(plugin_dir):
        for file in files:
            if file.endswith('.pyc') and 'maya_mcp' in file:
                pyc_path = os.path.join(root, file)
                try:
                    os.remove(pyc_path)
                    print(f"   Removed: {pyc_path}")
                except:
                    print(f"   Could not remove: {pyc_path}")
    
    # Step 4: Reload plugin
    print("\n4. Loading plugin...")
    try:
        cmds.loadPlugin(plugin_path)
        print("   Plugin loaded successfully!")
    except Exception as e:
        print(f"   ERROR loading plugin: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("Plugin reload complete!")
    print("=" * 60)
    return True

# Run the reload
if __name__ == "__main__":
    force_reload_plugin()