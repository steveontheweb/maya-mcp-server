"""
Maya MCP Plugin
Connect Maya to Claude AI through the Model Context Protocol (MCP)
"""

import maya.cmds as cmds
import maya.OpenMaya as om
import maya.mel as mel
import json
import socket
import threading
import traceback
import time
import tempfile
import os

# Plugin Configuration
DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 9877

class MayaMCPClient:
    """Maya MCP Socket Client - Runs inside Maya to handle MCP requests"""
    
    def __init__(self, host='localhost', port=9877):
        self.host = host
        self.port = port
        self.running = False
        self.socket = None
        self.server_thread = None
        
    def start(self):
        """Start the client socket listener"""
        if self.running:
            print("MayaMCP: The client is already running.")
            return
            
        self.running = True
        
        try:
            # Create socket
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.host, self.port))
            self.socket.listen(1)
            
            # Start client listener thread
            self.server_thread = threading.Thread(target=self._server_loop)
            self.server_thread.daemon = True
            self.server_thread.start()
            
            print(f"MayaMCP: Client started listening on {self.host}:{self.port}")
        except Exception as e:
            print(f"MayaMCP: Failed to start client: {str(e)}")
            self.stop()
            
    def stop(self):
        """Stop the client"""
        self.running = False
        
        # Close socket
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
            self.socket = None
            
        # Wait for thread to finish
        if self.server_thread:
            try:
                if self.server_thread.is_alive():
                    self.server_thread.join(timeout=1.0)
            except:
                pass
            self.server_thread = None
            
        print("MayaMCP: Client stopped")
        
    def _server_loop(self):
        """Main client listener loop"""
        print("MayaMCP: Client listener thread started")
        self.socket.settimeout(1.0)
        
        while self.running:
            try:
                try:
                    client, address = self.socket.accept()
                    print(f"MayaMCP: Connection accepted from: {address}")
                    
                    # Handle connection in separate thread
                    client_thread = threading.Thread(
                        target=self._handle_client,
                        args=(client,)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                except socket.timeout:
                    continue
                except Exception as e:
                    print(f"MayaMCP: Error accepting connection: {str(e)}")
                    time.sleep(0.5)
            except Exception as e:
                print(f"MayaMCP: Client loop error: {str(e)}")
                if not self.running:
                    break
                time.sleep(0.5)
                
        print("MayaMCP: Client listener thread stopped")
        
    def _handle_client(self, client):
        """Handle incoming connection with improved error handling"""
        print("MayaMCP: Connection handler started")
        client.settimeout(180.0)  # 3 minute timeout
        buffer = b''
        max_buffer_size = 10 * 1024 * 1024  # 10MB max buffer
        
        try:
            while self.running:
                try:
                    # Check buffer size
                    if len(buffer) > max_buffer_size:
                        print("MayaMCP: Buffer overflow protection triggered")
                        response = {
                            "status": "error",
                            "message": "Request too large. Maximum 10MB allowed."
                        }
                        try:
                            client.sendall(json.dumps(response).encode('utf-8'))
                        except:
                            pass
                        break
                    
                    data = client.recv(8192)
                    if not data:
                        print("MayaMCP: Connection closed")
                        break
                    
                    buffer += data
                    
                    # Check if complete JSON received
                    try:
                        # Try to parse command
                        command = json.loads(buffer.decode('utf-8'))
                        buffer = b''
                        
                        print(f"MayaMCP: Executing command: {command.get('type', 'unknown')}")
                        
                        # Execute command with error handling
                        try:
                            response = self.execute_command(command)
                        except Exception as cmd_error:
                            print(f"MayaMCP: Command execution error: {str(cmd_error)}")
                            response = {
                                "status": "error",
                                "message": str(cmd_error)
                            }
                        
                        response_json = json.dumps(response, ensure_ascii=False)
                        
                        try:
                            client.sendall(response_json.encode('utf-8'))
                            print("MayaMCP: Response sent successfully")
                        except Exception as send_error:
                            print(f"MayaMCP: Failed to send response: {str(send_error)}")
                            break
                            
                    except json.JSONDecodeError:
                        # Incomplete data, wait for more
                        if len(buffer) > 1024:  # Only log when buffer is large
                            print(f"MayaMCP: Waiting for more data... (buffer: {len(buffer)} bytes)")
                        continue
                        
                except socket.timeout:
                    print("MayaMCP: Socket timeout - closing connection")
                    break
                except Exception as e:
                    print(f"MayaMCP: Error receiving data: {str(e)}")
                    import traceback
                    traceback.print_exc()
                    break
                    
        except Exception as e:
            print(f"MayaMCP: Connection handler error: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            try:
                client.close()
            except:
                pass
            print("MayaMCP: Connection handler stopped")
            
    def execute_command(self, command):
        """Execute command in Maya main thread with performance monitoring"""
        start_time = time.time()
        
        try:
            cmd_type = command.get("type")
            params = command.get("params", {})
            
            print(f"MayaMCP: Processing command '{cmd_type}'...")
            
            # Command routing
            if cmd_type == "get_scene_info":
                result = self._get_scene_info()
            elif cmd_type == "get_object_info":
                result = self._get_object_info(params)
            elif cmd_type == "execute_code":
                result = self._execute_code(params)
            elif cmd_type == "create_primitive":
                result = self._create_primitive(params)
            elif cmd_type == "delete_object":
                result = self._delete_object(params)
            elif cmd_type == "set_material":
                result = self._set_material(params)
            elif cmd_type == "transform_object":
                result = self._transform_object(params)
            elif cmd_type == "get_viewport_screenshot":
                result = self._get_viewport_screenshot(params)
            elif cmd_type == "smart_select":
                result = self._smart_select(params)
            else:
                return {
                    "status": "error",
                    "message": f"Unknown command type: {cmd_type}"
                }
            
            execution_time = time.time() - start_time
            print(f"MayaMCP: Command '{cmd_type}' completed in {execution_time:.3f}s")
            
            if execution_time > 30:
                print(f"MayaMCP: WARNING - Command took longer than expected: {execution_time:.3f}s")
            
            return {
                "status": "success",
                "result": result,
                "execution_time": f"{execution_time:.3f}s"
            }
        except Exception as e:
            execution_time = time.time() - start_time
            error_msg = str(e)
            print(f"MayaMCP: Error executing command after {execution_time:.3f}s: {error_msg}")
            traceback.print_exc()
            return {
                "status": "error",
                "message": error_msg,
                "execution_time": f"{execution_time:.3f}s"
            }
            
    def _get_scene_info(self):
        """Get scene information"""
        try:
            # Get all DAG objects
            all_objects = cmds.ls(dagObjects=True, long=True) or []
            
            # Filter transform nodes
            transforms = cmds.ls(type='transform', long=True) or []
            
            # Get cameras
            cameras = cmds.ls(type='camera', long=True) or []
            
            # Get lights
            lights = cmds.ls(lights=True, long=True) or []
            
            # Get materials
            materials = cmds.ls(materials=True) or []
            
            # Get current selection
            selection = cmds.ls(selection=True, long=True) or []
            
            scene_info = {
                "total_objects": len(all_objects),
                "transforms": len(transforms),
                "cameras": len(cameras),
                "lights": len(lights),
                "materials": len(materials),
                "object_list": transforms[:50],  # Limit returned count
                "current_time": cmds.currentTime(query=True),
                "fps": mel.eval('currentTimeUnitToFPS()'),
                "selection": selection
            }
            
            return scene_info
        except Exception as e:
            import traceback
            error_msg = f"Failed to get scene info: {str(e)}\n{traceback.format_exc()}"
            print(f"MayaMCP: {error_msg}")
            raise Exception(error_msg)
            
    def _get_object_info(self, params):
        """Get detailed object information"""
        try:
            obj_name = params.get("name")
            if not obj_name:
                raise Exception("Object name not provided")
                
            if not cmds.objExists(obj_name):
                raise Exception(f"Object does not exist: {obj_name}")
                
            # Get object type
            obj_type = cmds.objectType(obj_name)
            
            # Get transform information
            translation = cmds.xform(obj_name, query=True, translation=True, worldSpace=True)
            rotation = cmds.xform(obj_name, query=True, rotation=True, worldSpace=True)
            scale = cmds.xform(obj_name, query=True, scale=True, relative=True)
            
            # Get bounding box
            bbox = cmds.exactWorldBoundingBox(obj_name)
            
            info = {
                "name": obj_name,
                "type": obj_type,
                "translation": translation,
                "rotation": rotation,
                "scale": scale,
                "bounding_box": {
                    "min": bbox[:3],
                    "max": bbox[3:]
                }
            }
            
            # Get material info if exists
            shape_nodes = cmds.listRelatives(obj_name, shapes=True, fullPath=True)
            if shape_nodes:
                shading_groups = cmds.listConnections(shape_nodes[0], type='shadingEngine')
                if shading_groups:
                    materials = cmds.ls(cmds.listConnections(shading_groups), materials=True)
                    if materials:
                        info["material"] = materials[0]
                        
            return info
        except Exception as e:
            raise Exception(f"Failed to get object info: {str(e)}")
            
    def _execute_code(self, params):
        """Execute Python code with safety limits and undo support"""
        try:
            code = params.get("code")
            if not code:
                raise Exception("Code not provided")
            
            # Check code length limit (prevent oversized code blocks)
            max_code_length = 50000  # 50KB
            if len(code) > max_code_length:
                raise Exception(f"Code too long. Maximum {max_code_length} characters allowed.")
            
            # Check for dangerous operations (basic safety check)
            dangerous_patterns = [
                'import subprocess', 'import os.system',
                'eval(', 'compile(',
                'execfile('
            ]
            code_lower = code.lower()
            for pattern in dangerous_patterns:
                if pattern in code_lower:
                    print(f"MayaMCP: Warning - potentially dangerous operation detected: {pattern}")
            
            # Create execution environment with standard builtins
            import sys
            import math
            import maya.utils as utils
            
            exec_globals = {
                'cmds': cmds,
                'om': om,
                'mel': mel,
                'math': math,
                'utils': utils,
                '__builtins__': __builtins__,
            }
            exec_locals = {}
            
            # Execute code with undo chunk and main thread safety
            start_time = time.time()
            execution_result = {'success': False, 'output': None, 'error': None}
            
            def execute_with_safety():
                """Execute code in main thread with undo support"""
                try:
                    # Open undo chunk for all operations
                    cmds.undoInfo(openChunk=True, chunkName='MCP_Code_Execution')
                    
                    try:
                        # Execute the code
                        exec(code, exec_globals, exec_locals)
                        execution_result['success'] = True
                        execution_result['output'] = exec_locals.get('result', 'Code executed successfully')
                    except Exception as exec_error:
                        # Close undo chunk on error (allows undo)
                        cmds.undoInfo(closeChunk=True)
                        # Undo the failed operations
                        cmds.undo()
                        execution_result['error'] = exec_error
                        execution_result['success'] = False
                        raise
                    finally:
                        # Always close the undo chunk
                        if cmds.undoInfo(query=True, chunkName=True):
                            cmds.undoInfo(closeChunk=True)
                        
                except Exception as e:
                    import traceback
                    execution_result['error'] = f"{str(e)}\n{traceback.format_exc()}"
                    raise
            
            # Execute in main thread for thread safety
            try:
                utils.executeInMainThreadWithResult(execute_with_safety)
            except Exception as thread_error:
                if execution_result['error']:
                    raise Exception(execution_result['error'])
                raise Exception(f"Thread execution error: {str(thread_error)}")
            
            execution_time = time.time() - start_time
            
            # Check execution time
            if execution_time > 60:
                print(f"MayaMCP: Warning - code execution took {execution_time:.2f}s")
            
            # Return result with full traceback on error
            if not execution_result['success']:
                raise Exception(execution_result['error'] if execution_result['error'] else "Unknown execution error")
            
            return {
                "output": str(execution_result['output']),
                "execution_time": f"{execution_time:.3f}s",
                "undo_available": True
            }
            
        except Exception as e:
            import traceback
            full_traceback = traceback.format_exc()
            error_msg = f"Failed to execute code: {str(e)}\n\nFull traceback:\n{full_traceback}"
            print(f"MayaMCP: {error_msg}")
            
            # Return detailed error for AI self-correction
            return {
                "output": "Error",
                "error": str(e),
                "traceback": full_traceback,
                "execution_time": f"{time.time() - start_time:.3f}s" if 'start_time' in locals() else "N/A",
                "undo_available": False
            }
            
    def _create_primitive(self, params):
        """Create primitive geometry"""
        try:
            prim_type = params.get("type", "cube")
            name = params.get("name")
            
            # Create geometry
            if prim_type == "cube":
                obj = cmds.polyCube(name=name)[0]
            elif prim_type == "sphere":
                obj = cmds.polySphere(name=name)[0]
            elif prim_type == "cylinder":
                obj = cmds.polyCylinder(name=name)[0]
            elif prim_type == "plane":
                obj = cmds.polyPlane(name=name)[0]
            elif prim_type == "torus":
                obj = cmds.polyTorus(name=name)[0]
            else:
                raise Exception(f"Unsupported geometry type: {prim_type}")
                
            # Apply transforms
            if "translation" in params:
                cmds.move(*params["translation"], obj)
            if "rotation" in params:
                cmds.rotate(*params["rotation"], obj)
            if "scale" in params:
                cmds.scale(*params["scale"], obj)
                
            return {"object": obj}
        except Exception as e:
            raise Exception(f"Failed to create primitive: {str(e)}")
            
    def _delete_object(self, params):
        """Delete object"""
        try:
            obj_name = params.get("name")
            if not obj_name:
                raise Exception("Object name not provided")
                
            if not cmds.objExists(obj_name):
                raise Exception(f"Object does not exist: {obj_name}")
                
            cmds.delete(obj_name)
            return {"message": f"Deleted object: {obj_name}"}
        except Exception as e:
            raise Exception(f"Failed to delete object: {str(e)}")
            
    def _set_material(self, params):
        """Set material"""
        try:
            obj_name = params.get("object")
            color = params.get("color", [1, 0, 0])  # Default red
            material_name = params.get("material_name", "material1")
            
            if not obj_name:
                raise Exception("Object name not provided")
                
            if not cmds.objExists(obj_name):
                raise Exception(f"Object does not exist: {obj_name}")
                
            # Create or get material
            if not cmds.objExists(material_name):
                material = cmds.shadingNode('lambert', asShader=True, name=material_name)
                shading_group = cmds.sets(renderable=True, noSurfaceShader=True,
                                        empty=True, name=f"{material_name}SG")
                cmds.connectAttr(f"{material}.outColor", f"{shading_group}.surfaceShader", force=True)
            else:
                material = material_name
                connections = cmds.listConnections(material, type='shadingEngine')
                if connections:
                    shading_group = connections[0]
                else:
                    shading_group = cmds.sets(renderable=True, noSurfaceShader=True,
                                            empty=True, name=f"{material_name}SG")
                    cmds.connectAttr(f"{material}.outColor", f"{shading_group}.surfaceShader", force=True)
                    
            # Set color
            cmds.setAttr(f"{material}.color", color[0], color[1], color[2], type="double3")
            
            # Apply material
            cmds.sets(obj_name, edit=True, forceElement=shading_group)
            
            return {"material": material, "shading_group": shading_group}
        except Exception as e:
            raise Exception(f"Failed to set material: {str(e)}")
            
    def _transform_object(self, params):
        """Transform object with parameter validation"""
        try:
            obj_name = params.get("object")
            if not obj_name:
                raise Exception("Object name not provided")
                
            if not cmds.objExists(obj_name):
                raise Exception(f"Object does not exist: {obj_name}")
            
            # Validate parameters before applying
            self._validate_transform_params(params)
            
            # Apply transforms with undo support
            cmds.undoInfo(openChunk=True, chunkName='Transform_Object')
            try:
                if "translation" in params:
                    cmds.move(*params["translation"], obj_name, absolute=True)
                if "rotation" in params:
                    cmds.rotate(*params["rotation"], obj_name, absolute=True)
                if "scale" in params:
                    cmds.scale(*params["scale"], obj_name, absolute=True)
                
                cmds.undoInfo(closeChunk=True)
                return {"message": f"Transformed object: {obj_name}", "undo_available": True}
            except Exception as e:
                cmds.undoInfo(closeChunk=True)
                cmds.undo()
                raise
                
        except Exception as e:
            raise Exception(f"Failed to transform object: {str(e)}")
            
    def _smart_select(self, params):
        """Smart selection based on query patterns and attributes"""
        try:
            query = params.get("query", "")
            select_type = params.get("type", "all")  # all, mesh, transform, etc.
            attribute_filter = params.get("attribute_filter", {})  # {"faces": ">5000"}
            
            print(f"MayaMCP: Smart select - query: '{query}', type: '{select_type}'")
            
            # Get objects based on type
            if select_type == "mesh":
                objects = cmds.ls(type='mesh', long=True)
            elif select_type == "transform":
                objects = cmds.ls(type='transform', long=True)
            elif select_type == "all":
                objects = cmds.ls(dag=True, long=True)
            else:
                objects = cmds.ls(type=select_type, long=True)
            
            # Filter by name pattern
            if query:
                import re
                pattern = re.compile(query, re.IGNORECASE)
                objects = [obj for obj in objects if pattern.search(obj)]
            
            # Filter by attributes
            filtered_objects = []
            for obj in objects:
                # Check vertex/face count for meshes
                if attribute_filter:
                    try:
                        if 'faces' in attribute_filter:
                            if cmds.objectType(obj) == 'mesh':
                                face_count = cmds.polyEvaluate(obj, face=True)
                                filter_expr = attribute_filter['faces']
                                
                                # Parse filter expression (e.g., ">5000", "<1000", "==500")
                                if filter_expr.startswith('>'):
                                    threshold = int(filter_expr[1:])
                                    if face_count > threshold:
                                        filtered_objects.append(obj)
                                elif filter_expr.startswith('<'):
                                    threshold = int(filter_expr[1:])
                                    if face_count < threshold:
                                        filtered_objects.append(obj)
                                elif filter_expr.startswith('=='):
                                    threshold = int(filter_expr[2:])
                                    if face_count == threshold:
                                        filtered_objects.append(obj)
                            continue
                        
                        # Add object if no face filter or already passed
                        filtered_objects.append(obj)
                    except:
                        # If attribute check fails, include the object
                        filtered_objects.append(obj)
                else:
                    filtered_objects = objects
            
            # Return with UUIDs to avoid name conflicts
            result_objects = []
            for obj in filtered_objects[:100]:  # Limit to 100 results
                try:
                    # Get UUID if possible
                    uuid = cmds.ls(obj, uuid=True)
                    result_objects.append({
                        'name': obj,
                        'uuid': uuid[0] if uuid else None,
                        'type': cmds.objectType(obj)
                    })
                except:
                    result_objects.append({
                        'name': obj,
                        'uuid': None,
                        'type': 'unknown'
                    })
            
            print(f"MayaMCP: Found {len(result_objects)} objects (showing max 100)")
            
            return {
                'objects': result_objects,
                'total_found': len(filtered_objects),
                'showing': len(result_objects)
            }
            
        except Exception as e:
            import traceback
            error_msg = f"Failed to smart select: {str(e)}\n{traceback.format_exc()}"
            print(f"MayaMCP: {error_msg}")
            raise Exception(error_msg)
    
    def _validate_transform_params(self, params):
        """Validate transform parameters to prevent Maya viewport crashes"""
        import math
        
        def validate_number(value, name, min_val=-1e6, max_val=1e6):
            """Validate a numeric value"""
            if value is None:
                return True
            
            if not isinstance(value, (int, float)):
                raise Exception(f"{name} must be a number, got {type(value)}")
            
            if math.isnan(value) or math.isinf(value):
                raise Exception(f"{name} contains NaN or Inf value")
            
            if value < min_val or value > max_val:
                raise Exception(f"{name} value {value} out of range [{min_val}, {max_val}]")
            
            return True
        
        def validate_vector(vector, name, min_val=-1e6, max_val=1e6):
            """Validate a 3D vector"""
            if vector is None:
                return True
            
            if not isinstance(vector, (list, tuple)) or len(vector) != 3:
                raise Exception(f"{name} must be a list/tuple of 3 numbers")
            
            for i, val in enumerate(vector):
                validate_number(val, f"{name}[{i}]", min_val, max_val)
            
            return True
        
        # Validate translation
        if 'translation' in params:
            validate_vector(params['translation'], 'translation')
        
        # Validate rotation (degrees)
        if 'rotation' in params:
            validate_vector(params['rotation'], 'rotation', -360000, 360000)
        
        # Validate scale (should be > 0 and reasonable)
        if 'scale' in params:
            scale = params['scale']
            if scale is not None:
                if not isinstance(scale, (list, tuple)) or len(scale) != 3:
                    raise Exception("scale must be a list/tuple of 3 numbers")
                for i, val in enumerate(scale):
                    validate_number(val, f"scale[{i}]", 0.0001, 10000)
        
        return True
    
    def _get_viewport_screenshot(self, params):
        """Capture viewport screenshot with enhanced error handling"""
        try:
            filepath = params.get("filepath")
            if not filepath:
                # Use temporary file
                temp_dir = tempfile.gettempdir()
                filepath = os.path.join(temp_dir, f"maya_screenshot_{int(time.time())}.jpg")
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            # Use safer screenshot method
            # Get current active 3D view panel
            panel = cmds.getPanel(withFocus=True)
            if not panel or cmds.getPanel(typeOf=panel) != 'modelPanel':
                # If current panel is not a 3D view, try to find one
                model_panels = cmds.getPanel(type='modelPanel')
                if model_panels:
                    panel = model_panels[0]
                else:
                    raise Exception("No 3D viewport found")
            
            # Use playblast to capture current frame
            # Remove file extension as Maya will add it automatically
            filepath_no_ext = os.path.splitext(filepath)[0]
            
            result_files = cmds.playblast(
                frame=[cmds.currentTime(query=True)],
                format='image',
                filename=filepath_no_ext,
                forceOverwrite=True,
                sequenceTime=False,
                clearCache=True,
                viewer=False,
                showOrnaments=False,
                offScreen=True,
                fp=4,
                percent=100,
                compression='jpg',
                quality=70,
                widthHeight=[800, 600]
            )
            
            # Maya may add frame numbers and extensions
            # Try to find the generated file
            actual_file = None
            if isinstance(result_files, list) and result_files:
                actual_file = result_files[0]
            elif isinstance(result_files, str):
                actual_file = result_files
            
            # Check if file exists
            if actual_file and os.path.exists(actual_file):
                # If filename differs, rename to requested filename
                if actual_file != filepath:
                    try:
                        if os.path.exists(filepath):
                            os.remove(filepath)
                        os.rename(actual_file, filepath)
                        actual_file = filepath
                    except:
                        pass
                return {"filepath": actual_file, "message": "Screenshot saved"}
            else:
                # Check for files with frame numbers
                import glob
                pattern = filepath_no_ext + "*"
                matching_files = glob.glob(pattern)
                if matching_files:
                    actual_file = matching_files[0]
                    if actual_file != filepath:
                        try:
                            if os.path.exists(filepath):
                                os.remove(filepath)
                            os.rename(actual_file, filepath)
                            actual_file = filepath
                        except:
                            pass
                    return {"filepath": actual_file, "message": "Screenshot saved"}
                else:
                    raise Exception("Screenshot file was not created")
                    
        except Exception as e:
            import traceback
            error_msg = f"Failed to capture screenshot: {str(e)}\n{traceback.format_exc()}"
            print(f"MayaMCP: {error_msg}")
            raise Exception(error_msg)

# Global client instance
_maya_mcp_client = None

def start_maya_mcp_client(host=DEFAULT_HOST, port=DEFAULT_PORT):
    """Start Maya MCP client"""
    global _maya_mcp_client
    
    if _maya_mcp_client and _maya_mcp_client.running:
        print("MayaMCP: Client is already running")
        return _maya_mcp_client
        
    _maya_mcp_client = MayaMCPClient(host=host, port=port)
    _maya_mcp_client.start()
    return _maya_mcp_client

def stop_maya_mcp_client():
    """Stop Maya MCP client"""
    global _maya_mcp_client
    
    if _maya_mcp_client:
        _maya_mcp_client.stop()
        _maya_mcp_client = None
        print("MayaMCP: Client stopped")
    else:
        print("MayaMCP: No client running")

# Maya plugin required functions
def initializePlugin(mobject):
    """
    Maya plugin initialization function
    Called when plugin is loaded
    """
    try:
        start_maya_mcp_client()
        print("MayaMCP: Plugin loaded successfully")
        print("MayaMCP: Client started listening on {}:{}".format(DEFAULT_HOST, DEFAULT_PORT))
        print("MayaMCP: To stop client, run: stop_maya_mcp_client()")
    except Exception as e:
        print("MayaMCP: Failed to initialize plugin: {}".format(str(e)))
        raise

def uninitializePlugin(mobject):
    """
    Maya plugin unload function
    Called when plugin is unloaded
    """
    try:
        stop_maya_mcp_client()
        print("MayaMCP: Plugin unloaded successfully")
    except Exception as e:
        print("MayaMCP: Failed to uninitialize plugin: {}".format(str(e)))

# If running directly in script editor (not loaded as plugin)
if __name__ == "__main__":
    start_maya_mcp_client()
    print("MayaMCP: Script executed, client started")
    print("MayaMCP: To stop client, run: stop_maya_mcp_client()")