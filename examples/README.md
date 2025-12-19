# Maya MCP 示例

本目录包含使用Maya MCP的各种示例和配置模板。

## 配置模板

### MCP配置文件

以下是三种不同的MCP服务器配置方式，选择最适合您的：

#### 1. mcp_config_npx.json - 使用npx（Node.js用户推荐）
适合已安装Node.js的用户，通过npx启动服务器。

**特点：**
- ✅ 统一Node.js生态
- ✅ 自动环境管理
- ✅ 需要Node.js

**配置内容：**
```json
{
  "mcpServers": {
    "maya-mcp": {
      "command": "npx",
      "args": [
        "--yes",
        "--package=D:/Program Files/maya-mcp-server",
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

#### 2. mcp_config_uvx.json - 使用uvx（Python用户推荐）
适合Python开发者，使用uv工具链。

**特点：**
- ✅ 纯Python工具
- ✅ 自动依赖管理
- ✅ 虚拟环境隔离

**配置内容：**
```json
{
  "mcpServers": {
    "maya-mcp": {
      "command": "uvx",
      "args": [
        "--from",
        "D:/Program Files/maya-mcp-server",
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

#### 3. mcp_config_python.json - 直接Python（开发调试）
直接运行Python模块，适合开发和调试。

**特点：**
- ✅ 最直接的方式
- ✅ 便于调试
- ⚠️ 需要手动设置PYTHONPATH

**配置内容：**
```json
{
  "mcpServers": {
    "maya-mcp": {
      "command": "python",
      "args": [
        "-m",
        "maya_mcp.server"
      ],
      "env": {
        "PYTHONPATH": "D:/Program Files/maya-mcp-server/src",
        "MAYA_HOST": "localhost",
        "MAYA_PORT": "9877"
      }
    }
  }
}
```

### 如何使用配置模板

1. **选择配置方式**：根据您的技术栈选择上面的一种配置

2. **复制配置内容**：复制对应json文件的内容

3. **修改路径**：将配置中的项目路径改为您的实际路径
   - 找到类似 `D:/Program Files/maya-mcp-server` 的路径
   - 替换为您的项目实际路径
   - 使用正斜杠 `/` 而不是反斜杠 `\`

4. **粘贴到MCP配置文件**：
   
   **Claude Desktop:**
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - 或在Claude中：Settings > Developer > Edit Config
   
   **Cursor:**
   - 全局：Settings > MCP
   - 项目：创建 `.cursor/mcp.json`

5. **保存并重启**：重启Claude Desktop或Cursor

### 配置对比

| 配置文件 | 工具 | 适合人群 | 优点 | 缺点 |
|---------|------|---------|------|------|
| [mcp_config_npx.json](mcp_config_npx.json) | npx | Node.js用户 | 统一生态、自动管理 | 需要Node.js |
| [mcp_config_uvx.json](mcp_config_uvx.json) | uvx | Python用户 | 纯Python、环境隔离 | 需要uv |
| [mcp_config_python.json](mcp_config_python.json) | python | 开发调试 | 直接、灵活 | 手动配置多 |

### 推荐配置

- 🟢 **有Node.js环境** → 使用 [mcp_config_npx.json](mcp_config_npx.json)
- 🟢 **纯Python开发** → 使用 [mcp_config_uvx.json](mcp_config_uvx.json)
- 🟡 **开发调试** → 使用 [mcp_config_python.json](mcp_config_python.json)

## 代码示例

### basic_usage.py
演示Maya MCP的基本Python API使用：
- 连接到Maya
- 获取场景信息
- 创建几何体
- 设置材质
- 变换对象
- 执行自定义代码

**运行方式：**
```bash
python basic_usage.py
```

**前提条件：**
- Maya正在运行
- Maya插件已启动

## 详细文档

- 📖 **npx配置指南**: [../doc/NPX_SETUP.md](../doc/NPX_SETUP.md)
- 📖 **完整MCP配置文档**: [../doc/MCP_CONFIG.md](../doc/MCP_CONFIG.md)
- 📖 **快速开始**: [../doc/QUICKSTART.md](../doc/QUICKSTART.md)
- 📖 **API文档**: [../doc/API.md](../doc/API.md)
- 📖 **使用指南**: [../doc/USAGE.md](../doc/USAGE.md)

## Claude使用示例

### 1. 创建简单场景

```
在Maya中创建一个简单的室内场景：
1. 创建一个大的平面作为地板，缩放为(10,1,10)
2. 创建四个立方体作为墙壁
3. 创建一个立方体作为桌子
4. 添加适当的颜色
5. 捕获截图
```

### 2. 几何体阵列

```
创建一个5x5的立方体网格，每个立方体之间间隔2个单位
```

### 3. 随机场景

```
执行以下代码创建随机场景：
- 创建20个随机大小的球体
- 随机分布在-10到10的范围内
- 每个球体使用随机颜色
```

### 4. 动画设置

```
创建一个球体，然后为其设置动画：
- 在第1帧，位置为(0,0,0)
- 在第24帧，位置为(10,5,0)
- 设置关键帧
```

### 5. 材质库

```
创建一个材质样本库：
- 创建10个球体排成一行
- 每个球体使用不同的颜色
- 从红色渐变到蓝色
```

## Maya脚本示例

### 批量创建对象

```python
import maya.cmds as cmds

# 创建网格
for i in range(5):
    for j in range(5):
        cube = cmds.polyCube(name=f'cube_{i}_{j}')[0]
        cmds.move(i*2, 0, j*2, cube)
        
        # 交替颜色
        if (i + j) % 2 == 0:
            color = [1, 0, 0]  # 红色
        else:
            color = [0, 0, 1]  # 蓝色
```

### 螺旋排列

```python
import maya.cmds as cmds
import math

# 创建螺旋排列的球体
num_spheres = 20
for i in range(num_spheres):
    angle = i * (360.0 / num_spheres) * (math.pi / 180.0)
    radius = 5 + i * 0.3
    
    x = radius * math.cos(angle)
    z = radius * math.sin(angle)
    y = i * 0.5
    
    sphere = cmds.polySphere(name=f'sphere_{i}')[0]
    cmds.move(x, y, z, sphere)
```

### 程序化建筑

```python
import maya.cmds as cmds

# 创建简单建筑
def create_building(x, z, floors=3):
    # 地基
    base = cmds.polyCube(name='base', w=4, h=0.5, d=4)[0]
    cmds.move(x, 0.25, z, base)
    
    # 楼层
    for floor in range(floors):
        y = 0.5 + floor * 3
        floor_obj = cmds.polyCube(name=f'floor_{floor}', w=4, h=2.8, d=4)[0]
        cmds.move(x, y + 1.4, z, floor_obj)
    
    # 屋顶
    roof = cmds.polyCube(name='roof', w=4.5, h=0.3, d=4.5)[0]
    cmds.move(x, 0.5 + floors * 3 + 0.15, z, roof)

# 创建建筑
create_building(0, 0, floors=5)
```

## 提示与技巧

### 1. 使用变量存储对象名称
```python
cube = cmds.polyCube()[0]
cmds.move(5, 0, 0, cube)
cmds.rotate(0, 45, 0, cube)
```

### 2. 使用循环创建多个对象
```python
for i in range(10):
    obj = cmds.polySphere()[0]
    cmds.move(i*2, 0, 0, obj)
```

### 3. 使用条件语句
```python
objects = cmds.ls(type='transform')
for obj in objects:
    if 'pCube' in obj:
        cmds.setAttr(f'{obj}.visibility', 0)
```

### 4. 错误处理
```python
try:
    cmds.delete('nonexistent_object')
except Exception as e:
    print(f"错误: {e}")
```

### 5. 选择和操作
```python
# 选择所有球体
spheres = cmds.ls('pSphere*')
for sphere in spheres:
    # 获取位置
    pos = cmds.xform(sphere, q=True, t=True, ws=True)
    # 如果在原点上方
    if pos[1] > 0:
        cmds.setAttr(f'{sphere}.translateY', pos[1] + 1)
```

## 调试技巧

### 检查连接
```python
from maya_mcp.server import get_maya_connection

maya = get_maya_connection()
result = maya.send_command("get_scene_info")
print(result)
```

### 测试命令
```python
# 测试简单命令
maya.send_command("create_primitive", {"type": "cube"})

# 测试复杂命令
maya.send_command("execute_code", {
    "code": "print('Hello from Maya')"
})
```

### 捕获错误
```python
try:
    result = maya.send_command("some_command", params)
except Exception as e:
    print(f"命令失败: {e}")
```

## 贡献示例

如果你有有趣的示例，欢迎贡献！

1. 创建新的示例文件
2. 添加详细注释
3. 更新此README
4. 提交Pull Request