# Maya MCP Server

**Conecta Claude AI a Autodesk Maya mediante Model Context Protocol**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Maya 2020+](https://img.shields.io/badge/maya-2020+-green.svg)](https://www.autodesk.com/products/maya/)

[English](README.md) | [简体中文](README_CN.md) | [繁體中文](README_CN_TW.md) | [日本語](README_JP.md) | [한국어](README_KO.md) | [Español](README_ES.md) | [Français](README_FR.md) | [Deutsch](README_DE.md) | [Русский](README_RU.md)

---

## Descripción General

Maya MCP Server permite que Claude AI controle directamente Autodesk Maya mediante Model Context Protocol, permitiendo:

- 🎨 Modelado 3D asistido por IA
- 🤖 Control de Maya con lenguaje natural
- 📸 Vista previa de escena en tiempo real
- 🔧 Automatización de flujo de trabajo

## Inicio Rápido

### 1. Instalar Dependencias

```bash
pip install "mcp[cli]>=1.3.0"
```

### 2. Cargar el Plugin de Maya

Carga `plug-ins/maya_mcp.py` en el **Administrador de Plugins** de Maya:

1. Copia `plug-ins/maya_mcp.py` a:
   - Windows: `C:\Users\<nombre_usuario>\Documents\maya\<versión>\plug-ins\`
   - macOS: `~/maya/<versión>/plug-ins/`

2. Abre Maya → **Windows > Settings/Preferences > Plug-in Manager**

3. Encuentra `maya_mcp.py`, marca **Loaded** y **Auto load**

4. Verifica en el Editor de Scripts:
   ```
   MayaMCP: Plugin cargado exitosamente
   MayaMCP: Servidor iniciado en localhost:9877
   ```

### 3. Configurar Claude Desktop

Edita el archivo de configuración (**Settings > Developer > Edit Config**):

#### Método A: Usando npx (Recomendado)

```json
{
  "mcpServers": {
    "maya-mcp": {
      "command": "npx",
      "args": [
        "--yes",
        "--package=ruta_del_proyecto",
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

#### Método B: Usando Python

```json
{
  "mcpServers": {
    "maya-mcp": {
      "command": "python",
      "args": ["-m", "maya_mcp.server"],
      "env": {
        "PYTHONPATH": "ruta_del_proyecto/src",
        "MAYA_HOST": "localhost",
        "MAYA_PORT": "9877"
      }
    }
  }
}
```

> 💡 Consulta el directorio [`examples/`](examples/) para más métodos de configuración

### 4. Probar la Conexión

Reinicia Claude Desktop y pregunta:

```
Obtener información de la escena actual de Maya
```

¡Si ves la información de la escena, la conexión fue exitosa! ✅

## Características

### 🛠️ Herramientas Principales

| Herramienta | Función |
|-----|------|
| `get_scene_info` | Obtener información de la escena (objetos, cámaras, luces) |
| `get_object_info` | Obtener detalles del objeto (posición, rotación, material) |
| `create_primitive` | Crear geometría (cube/sphere/cylinder/plane/torus) |
| `delete_object` | Eliminar objeto |
| `transform_object` | Transformar objeto (mover/rotar/escalar) |
| `set_material` | Establecer material y color |
| `execute_maya_code` | Ejecutar código Python |
| `get_viewport_screenshot` | Capturar captura de pantalla del viewport ⚠️ |
| `smart_select` | Selección inteligente de objetos con regex y filtros |
| `get_scene_summary` | Obtener resumen completo de la escena |
| `get_console_output` | Obtener salida de consola/editor de scripts de Maya 🆕 |

> ⚠️ Nota: `get_viewport_screenshot` puede ser inestable en algunas versiones de Maya debido a problemas de compatibilidad con playblast.

### 💬 Ejemplos de Conversación

```
Usuario: Crea un cubo rojo en la posición (0, 5, 0)

Claude:
1. Creé el cubo
2. Lo moví a la posición especificada
3. Apliqué material rojo
✅ Completado
```

```
Usuario: Crea una escena simple de mesa y silla y toma una captura de pantalla

Claude:
1. Creé la superficie de la mesa (cubo escalado)
2. Creé 4 patas de mesa (cilindros)
3. Creé la silla
4. Establecí los materiales
5. Capturé la captura de pantalla del viewport
✅ [Mostrando captura de pantalla]
```

## Ejemplos de Uso

### Operaciones Básicas

```
# Consultas de escena
"Mostrar todos los objetos en la escena actual"
"Obtener información detallada de pCube1"
"Obtener salida de consola para ver registros recientes de Maya"

# Crear objetos
"Crear una esfera llamada mySphere"
"Crear 10 cubos en una fila"

# Modificar objetos
"Mover pCube1 a (5, 0, 0)"
"Establecer pSphere1 en azul"
"Rotar pCylinder1 45 grados en el eje Y"

# Selección inteligente
"Seleccionar todos los objetos con 'character' en su nombre"
"Encontrar todas las mallas con más de 5000 caras"
```

### Operaciones Avanzadas

```
# Modelado procedimental
"Ejecutar código para crear una cuadrícula de cubos 5x5"

# Edición de vértices/caras
"Crear un plano y editar vértices para hacer un terreno"
"Extruir caras para crear detalles"

# Edición UV
"Aplicar proyección UV automática a objetos seleccionados"
"Crear mapeo UV esférico para la esfera"

# Animación
"Crear animación de fotogramas clave para pelota rebotando"
"Configurar sistema de iluminación de 3 puntos"

# Rigging
"Crear cadena de huesos de columna vertebral con 5 articulaciones"
"Configurar restricciones de padre"

# Dinámica
"Crear sistema de partículas con gravedad"
"Aplicar deformador de doblado al plano"

# Operaciones booleanas
"Restar cube2 de cube1"
"Unir dos esferas superpuestas"

# Operaciones por lotes
"Establecer colores aleatorios para todas las esferas"

# Escenas complejas
"Crear una escena interior simple con piso, paredes y muebles"
```

## Opciones de Configuración

### Variables de Entorno

| Variable | Valor Predeterminado | Descripción |
|------|--------|------|
| `MAYA_HOST` | `localhost` | Dirección del servidor Maya |
| `MAYA_PORT` | `9877` | Puerto del servidor Maya |
| `PYTHONPATH` | - | Ruta de búsqueda de módulos Python (solo para modo Python directo) |

### Puerto Personalizado

**Modificar en el plugin de Maya:**
```python
start_maya_mcp_server(host='localhost', port=9878)
```

**Modificar en el archivo de configuración:**
```json
"env": {
  "MAYA_PORT": "9878"
}
```

## Solución de Problemas

### Fallo de Conexión

**Problema:** "No se puede conectar a Maya"

**Solución:**
1. ✅ Confirma que Maya está en ejecución
2. ✅ Confirma que el plugin está cargado (verifica el Administrador de Plugins)
3. ✅ Verifica el mensaje de inicio en el Editor de Scripts
4. ✅ Confirma que el puerto 9877 no está en uso

### Módulo No Encontrado

**Problema:** "ModuleNotFoundError: No module named 'maya_mcp'"

**Solución:**
1. Instala las dependencias: `pip install "mcp[cli]>=1.3.0"`
2. Verifica la configuración de PYTHONPATH (si usas el modo Python directo)
3. Intenta usar el método npx

### Fallo al Cargar el Plugin

**Problema:** Maya reporta "No initializePlugin() function"

**Solución:**
- Asegúrate de usar la versión más reciente de `maya_mcp.py`
- El archivo del plugin debe contener las funciones `initializePlugin()` y `uninitializePlugin()`

## Avisos de Seguridad

⚠️ **Nota Importante:**

- La herramienta `execute_maya_code` permite ejecutar código Python arbitrario
- Siempre **guarda tu escena de Maya** antes de ejecutar
- Usa con precaución en entornos de producción
- Se recomienda verificar las operaciones en escenas de prueba primero

## Registros

Los registros del servidor se guardan en:
- **Windows:** `%TEMP%\maya-mcp\maya-mcp.log`
- **macOS/Linux:** `/tmp/maya-mcp/maya-mcp.log`

Revisa los registros para depurar problemas de conexión o errores de ejecución de comandos.

## Desarrollo

### Agregar Nuevas Herramientas

1. Agrega el manejador de comandos en `plug-ins/maya_mcp.py`
2. Agrega la definición de herramienta MCP en `src/maya_mcp/server.py`
3. Prueba la nueva herramienta

### Ejecutar el Servidor de Desarrollo

```bash
# Configurar entorno
export PYTHONPATH=/path/to/maya-mcp-server/src

# Ejecutar servidor
python -m maya_mcp.server
```

## Contribuciones

¡Las contribuciones son bienvenidas! Consulta [`CONTRIBUTING.md`](CONTRIBUTING.md)

## Agradecimientos

Este proyecto está inspirado en:
- [Blender-MCP](https://github.com/ahujasid/blender-mcp) - Referencia de diseño de arquitectura

## Licencia

[MIT License](LICENSE)

## Descargo de Responsabilidad

Este es un proyecto de terceros, no un producto oficial de Autodesk.

---

<div align="center">

**[Comenzar](examples/)** • **[Guía de Configuración](examples/README.md)** • **[Reportar Problema](../../issues)**

Hecho con ❤️ para artistas de Maya y entusiastas de la IA

</div>