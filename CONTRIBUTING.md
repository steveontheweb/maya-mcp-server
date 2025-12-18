# 为Maya MCP做贡献

感谢您对Maya MCP项目的关注！我们欢迎各种形式的贡献。

## 如何贡献

### 报告Bug

如果您发现了bug，请创建一个issue并包含：

1. **清晰的标题**：简短描述问题
2. **详细描述**：
   - 您期望发生什么
   - 实际发生了什么
   - 重现步骤
3. **环境信息**：
   - Maya版本
   - Python版本
   - 操作系统
   - Maya MCP版本
4. **日志输出**：相关的错误消息或日志
5. **截图**（如适用）

### 功能请求

对于新功能建议，请创建issue并说明：

1. **用例**：为什么需要这个功能
2. **提议的解决方案**：您认为应该如何实现
3. **替代方案**：您考虑过的其他方法

### 提交代码

1. **Fork仓库**
2. **创建分支**：`git checkout -b feature/your-feature-name`
3. **进行更改**
4. **测试更改**
5. **提交**：`git commit -m "描述性的提交信息"`
6. **推送**：`git push origin feature/your-feature-name`
7. **创建Pull Request**

## 开发设置

### 前置条件

- Python 3.10+
- Maya 2020+
- uv包管理器

### 本地开发环境

```bash
# 克隆仓库
git clone https://github.com/Jeffreytsai1004/maya-mcp-server.git
cd maya-mcp

# 安装依赖
uv pip install -e .

# 在Maya中加载插件
# 在Maya脚本编辑器中执行maya_plugin.py
```

## 代码规范

### Python代码风格

- 遵循PEP 8
- 使用4个空格缩进
- 函数和方法使用docstring
- 类型提示（当适用时）

**示例：**
```python
def transform_object(
    object_name: str,
    translation: list = None,
    rotation: list = None
) -> Dict[str, Any]:
    """
    变换Maya对象。
    
    参数:
        object_name: 对象名称
        translation: 位置[x, y, z]
        rotation: 旋转[x, y, z]（度）
    
    返回:
        包含结果的字典
    """
    # 实现
```

### 提交消息

使用清晰的提交消息：

```
类型: 简短描述（50字符以内）

详细描述（如需要）

- 要点1
- 要点2
```

**类型：**
- `feat`: 新功能
- `fix`: Bug修复
- `docs`: 文档更改
- `style`: 格式化（不影响代码含义）
- `refactor`: 重构
- `test`: 添加测试
- `chore`: 维护任务

## 测试

### 运行测试

```bash
# 单元测试
python -m pytest tests/

# 集成测试（需要Maya运行）
python tests/integration_test.py
```

### 编写测试

为新功能添加测试：

```python
def test_create_primitive():
    """测试创建基本几何体"""
    maya = get_maya_connection()
    result = maya.send_command("create_primitive", {
        "type": "cube",
        "name": "testCube"
    })
    assert "object" in result
    assert "testCube" in result["object"]
```

## 文档

### 更新文档

如果您的更改影响用户，请更新相应文档：

- `README.md`: 项目概述和基本说明
- `doc/USAGE.md`: 使用指南
- `doc/API.md`: API参考
- `doc/QUICKSTART.md`: 快速入门
- `doc/ARCHITECTURE.md`: 架构设计

### 文档风格

- 使用清晰的标题层次
- 提供代码示例
- 包含截图（当有帮助时）
- 保持简洁明了

## 添加新工具

### 1. 在Maya插件中实现

在`maya_plugin.py`中添加命令处理器：

```python
def _my_new_command(self, params):
    """
    执行新命令
    
    参数:
        params: 命令参数字典
    
    返回:
        结果字典
    """
    try:
        # 实现逻辑
        param1 = params.get("param1")
        # ... 处理
        return {"result": "成功"}
    except Exception as e:
        raise Exception(f"命令失败: {str(e)}")
```

在命令路由中添加：

```python
elif cmd_type == "my_new_command":
    result = self._my_new_command(params)
```

### 2. 在MCP服务器中添加工具

在`src/maya_mcp/server.py`中：

```python
@mcp.tool()
def my_new_tool(ctx: Context, param1: str) -> str:
    """
    我的新工具描述
    
    参数:
    - param1: 参数描述
    """
    try:
        maya = get_maya_connection()
        result = maya.send_command("my_new_command", {
            "param1": param1
        })
        return json.dumps(result, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.error(f"工具执行错误: {str(e)}")
        return f"错误: {str(e)}"
```

### 3. 添加文档

在`doc/API.md`中记录新工具：

```markdown
### my_new_tool

工具描述

**参数：**
- `param1`: 参数描述

**返回：**
结果描述

**使用示例：**
```
使用我的新工具进行xxx
```
```

### 4. 添加测试

创建测试用例：

```python
def test_my_new_tool():
    """测试新工具"""
    maya = get_maya_connection()
    result = maya.send_command("my_new_command", {
        "param1": "test_value"
    })
    assert result["result"] == "成功"
```

## 代码审查流程

Pull Request将被审查：

1. **代码质量**：是否遵循编码规范
2. **功能性**：是否按预期工作
3. **测试**：是否包含适当的测试
4. **文档**：是否更新了相关文档
5. **向后兼容性**：是否破坏现有功能

## 发布流程

1. 更新版本号（`pyproject.toml`）
2. 更新CHANGELOG
3. 创建Git标签
4. 构建包：`python -m build`
5. 发布到PyPI：`twine upload dist/*`

## 社区准则

### 行为准则

- 尊重所有贡献者
- 建设性的批评
- 专注于最佳解决方案
- 欢迎新手

### 沟通渠道

- GitHub Issues：Bug报告和功能请求
- GitHub Discussions：一般讨论
- Pull Requests：代码贡献

## 获得帮助

如果您需要帮助：

1. 查看[文档](doc/)
2. 搜索现有issues
3. 创建新issue描述您的问题
4. 在discussions中提问

## 许可证

贡献的代码将在MIT许可证下发布。

## 致谢

感谢所有为这个项目做出贡献的人！

---

再次感谢您的贡献！🎉