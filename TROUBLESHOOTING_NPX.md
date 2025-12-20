# NPX 故障排除指南

## 常见问题和解决方案

### 1. npx 命令找不到包

**问题**: `npx maya-mcp-server` 报错 "package not found"

**解决方案**:
```bash
# 方法1: 使用本地包
npx --package=file:./path/to/maya-mcp-server maya-mcp-server

# 方法2: 先安装再运行
npm install -g maya-mcp-server
maya-mcp-server

# 方法3: 使用完整路径
npx --package=file:H:/path/to/maya-mcp-server maya-mcp-server
```

### 2. Python 模块找不到

**问题**: `ModuleNotFoundError: No module named 'maya_mcp'`

**解决方案**:
1. 确保 `src/maya_mcp/__main__.py` 文件存在
2. 检查 PYTHONPATH 设置
3. 验证 Python 版本 >= 3.10

```bash
# 检查 Python 版本
python --version

# 手动测试 Python 模块
cd /path/to/maya-mcp-server
python -m maya_mcp.server
```

### 3. MCP 配置问题

**正确的 MCP 配置**:

#### 全局安装后使用:
```json
{
  "mcpServers": {
    "maya-mcp": {
      "command": "maya-mcp-server",
      "env": {
        "MAYA_HOST": "localhost",
        "MAYA_PORT": "9877"
      }
    }
  }
}
```

#### 使用 npx:
```json
{
  "mcpServers": {
    "maya-mcp": {
      "command": "npx",
      "args": ["--yes", "maya-mcp-server"],
      "env": {
        "MAYA_HOST": "localhost",
        "MAYA_PORT": "9877"
      }
    }
  }
}
```

#### 本地开发使用:
```json
{
  "mcpServers": {
    "maya-mcp": {
      "command": "npx",
      "args": [
        "--yes", 
        "--package=file:./path/to/maya-mcp-server",
        "maya-mcp-server"
      ],
      "env": {
        "MAYA_HOST": "localhost",
        "MAYA_PORT": "9877"
      }
    }
  }
}
```

### 4. 权限问题

**Windows 用户**:
- 确保以管理员身份运行终端
- 检查防火墙设置
- 确保 Maya 命令端口已启用

**macOS/Linux 用户**:
- 检查文件权限: `chmod +x bin/maya-mcp.js`
- 确保 Python 可执行

### 5. Maya 连接问题

**检查 Maya 设置**:
1. 打开 Maya
2. 进入 **Windows > Settings/Preferences > Preferences**
3. 选择 **Interface > Command Ports**
4. 确保启用 "MEL" 端口 9877

**测试连接**:
```python
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock.connect(('localhost', 9877))
    print("Maya 连接成功")
except:
    print("Maya 连接失败")
finally:
    sock.close()
```

### 6. 调试步骤

1. **验证包结构**:
   ```bash
   node test_npm_setup.js
   ```

2. **手动测试 Node.js 入口**:
   ```bash
   node bin/maya-mcp.js
   ```

3. **手动测试 Python 模块**:
   ```bash
   python -m maya_mcp.server
   ```

4. **检查日志文件**:
   - Windows: `%TEMP%\maya-mcp\maya-mcp.log`
   - macOS/Linux: `/tmp/maya-mcp/maya-mcp.log`

### 7. 环境变量

设置这些环境变量可能有帮助:
```bash
# Windows
set MAYA_HOST=localhost
set MAYA_PORT=9877
set PYTHONPATH=%CD%\src

# macOS/Linux
export MAYA_HOST=localhost
export MAYA_PORT=9877
export PYTHONPATH=$PWD/src
```

### 8. 常见错误信息

| 错误信息 | 可能原因 | 解决方案 |
|---------|---------|---------|
| `ENOENT: no such file` | 路径错误 | 检查文件路径 |
| `Permission denied` | 权限问题 | 以管理员运行 |
| `Module not found` | Python 路径问题 | 检查 PYTHONPATH |
| `Connection refused` | Maya 未启动 | 启动 Maya 并启用命令端口 |
| `Port already in use` | 端口冲突 | 更改端口或关闭占用进程 |

如果问题仍然存在，请提供完整的错误日志以便进一步诊断。