# Maya MCP Server

**通过Model Context Protocol将Claude AI连接到Autodesk Maya**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Maya 2020+](https://img.shields.io/badge/maya-2020+-green.svg)](https://www.autodesk.com/products/maya/)

[English](README.md) | [简体中文](README_CN.md) | [繁體中文](README_CN_TW.md) | [日本語](README_JP.md) | [한국어](README_KO.md) | [Español](README_ES.md) | [Français](README_FR.md) | [Deutsch](README_DE.md) | [Русский](README_RU.md)

---

## 概述

Maya MCP Server使Claude AI能够通过Model Context Protocol直接控制Autodesk Maya，实现：

- 🎨 AI辅助3D建模
- 🤖 自然语言控制Maya
- 📸 实时场景预览
- 🔧 工作流程自动化

## 快速开始

### 1. 安装依赖

```bash
pip install "mcp[cli]>=1.3.0"
```

### 2. 加载Maya插件

在Maya的**插件管理器**中加载 `plug-ins/maya_mcp.py`：

1. 将 `plug-ins/maya_mcp.py` 复制到：
   - Windows: `C:\Users\<用户名>\Documents\maya\<版本>\plug-ins\`
   - macOS: `~/maya/<版本>/plug-ins/`

2. 打开Maya → **Windows > Settings/Preferences > Plug-in Manager**

3. 找到 `maya_mcp.py`，勾选 **Loaded** 和 **Auto load**

4. 在脚本编辑器中确认：
   ```
   MayaMCP: 插件已成功加载
   MayaMCP: 服务器已启动在 localhost:9877
   ```

### 3. 配置Claude Desktop

编辑配置文件（**Settings > Developer > Edit Config**）：

#### 方式A：使用npx（推荐）

**标准配置：**
```json
{
  "mcpServers": {
    "maya-mcp": {
      "command": "npx",
      "args": [
        "--yes",
        "maya-mcp-server"
      ],
      "env": {
        "MAYA_HOST": "localhost",
        "MAYA_PORT": "9877"
      },
      "alwaysAllow": [
          "get_scene_info",
          "get_object_info",
          "create_primitive",
          "delete_object",
          "set_material",
          "transform_object",
          "smart_select",
          "get_scene_summary",
          "get_console_output",
          "execute_maya_code"
      ]
    }
  }
}
```

**强制更新配置（每次启动时拉取最新包）：**
```json
{
  "mcpServers": {
    "maya-mcp": {
      "command": "npx",
      "args": [
        "--yes",
        "--no-cache",
        "maya-mcp-server"
      ],
      "env": {
        "MAYA_HOST": "localhost",
        "MAYA_PORT": "9877"
      },
      "alwaysAllow": [
          "get_scene_info",
          "get_object_info",
          "create_primitive",
          "delete_object",
          "set_material",
          "transform_object",
          "smart_select",
          "get_scene_summary",
          "get_console_output",
          "execute_maya_code"
      ]
    }
  }
}
```

#### 方式B：使用Python

```json
{
  "mcpServers": {
    "maya-mcp": {
      "command": "python",
      "args": ["-m", "maya_mcp.server"],
      "env": {
        "PYTHONPATH": "你的项目路径/src",
        "MAYA_HOST": "localhost",
        "MAYA_PORT": "9877"
      },
      "alwaysAllow": [
          "get_scene_info",
          "create_primitive",
          "delete_object",
          "set_material",
          "transform_object",
          "smart_select",
          "get_scene_summary",
          "get_console_output",
          "execute_maya_code"
      ]
    }
  }
}
```

> 💡 更多配置方式请查看 [`examples/`](examples/) 目录

### 4. 测试连接

重启Claude Desktop，然后询问：

```
获取当前Maya场景信息
```

如果看到场景信息返回，说明连接成功！✅

## 功能特性

### 🛠️ 核心工具

| 工具 | 功能 |
|-----|------|
| `get_scene_info` | 获取场景信息（对象、相机、灯光） |
| `get_object_info` | 获取对象详情（位置、旋转、材质） |
| `create_primitive` | 创建几何体（cube/sphere/cylinder/plane/torus） |
| `delete_object` | 删除对象 |
| `transform_object` | 变换对象（移动/旋转/缩放） |
| `set_material` | 设置材质和颜色 |
| `execute_maya_code` | 执行Python代码 |
| `smart_select` | 智能对象选择（支持正则和过滤） |
| `get_scene_summary` | 获取全面的场景摘要 |
| `get_console_output` | 获取Maya控制台/脚本编辑器输出 🆕 |

### 💬 示例对话

```
用户：创建一个红色的立方体，位置在(0, 5, 0)

Claude：
1. 创建了立方体
2. 移动到指定位置
3. 应用了红色材质
✅ 完成
```

```
用户：创建一个简单的桌椅场景

Claude：
1. 创建了桌面（缩放后的立方体）
2. 创建了4个桌腿（圆柱体）
3. 创建了椅子
4. 设置了材质
```

## 使用示例

### 基础操作

```
# 场景查询
"显示当前场景的所有对象"
"获取pCube1的详细信息"
"获取控制台输出查看最近的Maya日志"

# 创建对象
"创建一个名为mySphere的球体"
"创建10个立方体排成一行"

# 修改对象
"将pCube1移动到(5, 0, 0)"
"将pSphere1设为蓝色"
"将pCylinder1在Y轴旋转45度"

# 智能选择
"选择所有名称包含'character'的对象"
"查找所有面数超过5000的网格"
```

### 高级操作

```
# 程序化建模
"执行代码创建一个5x5的立方体网格"

# 顶点/面编辑
"创建一个平面并编辑顶点制作地形"
"挤出面来创建细节"

# UV编辑
"为选中对象应用自动UV投影"
"为球体创建球形UV映射"

# 动画
"为弹跳球创建关键帧动画"
"设置三点照明系统"

# 绑定
"创建包含5个关节的脊椎骨骼链"
"设置父约束"

# 动力学
"创建带重力的粒子系统"
"为平面应用弯曲变形器"

# 布尔运算
"从cube1中减去cube2"
"合并两个重叠的球体"

# 批量操作
"为所有球体设置随机颜色"

# 复杂场景
"创建一个简单的室内场景，包含地板、墙壁和家具"
```

## 配置选项

### 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `MAYA_HOST` | `localhost` | Maya服务器地址 |
| `MAYA_PORT` | `9877` | Maya服务器端口 |
| `PYTHONPATH` | - | Python模块搜索路径（仅Python直接模式需要） |

### 自定义端口

**在Maya插件中修改：**
```python
start_maya_mcp_server(host='localhost', port=9878)
```

**在配置文件中修改：**
```json
"env": {
  "MAYA_PORT": "9878"
}
```

## 故障排除

### 连接失败

**问题：** "无法连接到Maya"

**解决方案：**
1. ✅ 确认Maya正在运行
2. ✅ 确认插件已加载（检查插件管理器）
3. ✅ 检查脚本编辑器中的启动消息
4. ✅ 确认端口9877未被占用

### 模块未找到

**问题：** "ModuleNotFoundError: No module named 'maya_mcp'"

**解决方案：**
1. 安装依赖：`pip install "mcp[cli]>=1.3.0"`
2. 检查PYTHONPATH设置（如使用Python直接模式）
3. 尝试使用npx方式

### 插件加载失败

**问题：** Maya报告"No initializePlugin() function"

**解决方案：**
- 确保使用最新版本的 `maya_mcp.py`
- 插件文件包含 `initializePlugin()` 和 `uninitializePlugin()` 函数

## 安全注意事项

⚠️ **重要提示：**

- `execute_maya_code` 工具允许执行任意Python代码
- 始终在执行前**保存Maya场景**
- 在生产环境中谨慎使用
- 建议先在测试场景中验证操作

## 日志

服务器日志保存在：
- **Windows:** `%TEMP%\maya-mcp\maya-mcp.log`
- **macOS/Linux:** `/tmp/maya-mcp/maya-mcp.log`

查看日志以调试连接问题或命令执行错误。

## 开发

### 添加新工具

1. 在 `plug-ins/maya_mcp.py` 中添加命令处理器
2. 在 `src/maya_mcp/server.py` 中添加MCP工具定义
3. 测试新工具

### 运行开发服务器

```bash
# 设置环境
set PYTHONPATH=d:/path/to/maya-mcp-server/src

# 运行服务器
python -m maya_mcp.server
```

## 贡献

欢迎贡献！请查看 [`CONTRIBUTING.md`](CONTRIBUTING.md)

## 致谢

本项目受以下项目启发：
- [Blender-MCP](https://github.com/ahujasid/blender-mcp) - 架构设计参考

## 许可证

[MIT License](LICENSE)

## 免责声明

这是一个第三方项目，非Autodesk官方产品。

---

<div align="center">

**[开始使用](examples/)** • **[配置指南](examples/README.md)** • **[问题反馈](../../issues)**

为Maya艺术家和AI爱好者倾心打造 ❤️

</div>