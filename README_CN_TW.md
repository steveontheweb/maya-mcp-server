# Maya MCP Server

**透過Model Context Protocol將Claude AI連接至Autodesk Maya**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Maya 2020+](https://img.shields.io/badge/maya-2020+-green.svg)](https://www.autodesk.com/products/maya/)

[English](README.md) | [简体中文](README_CN.md) | [繁體中文](README_CN_TW.md) | [日本語](README_JP.md) | [한국어](README_KO.md) | [Español](README_ES.md) | [Français](README_FR.md) | [Deutsch](README_DE.md) | [Русский](README_RU.md)

---

## 概述

Maya MCP Server使Claude AI能夠透過Model Context Protocol直接控制Autodesk Maya，實現：

- 🎨 AI輔助3D建模
- 🤖 自然語言控制Maya
- 📸 即時場景預覽
- 🔧 工作流程自動化

## 快速開始

### 1. 安裝相依套件

```bash
pip install "mcp[cli]>=1.3.0"
```

### 2. 載入Maya外掛

在Maya的**外掛管理器**中載入 `plug-ins/maya_mcp.py`：

1. 將 `plug-ins/maya_mcp.py` 複製到：
   - Windows: `C:\Users\<使用者名稱>\Documents\maya\<版本>\plug-ins\`
   - macOS: `~/maya/<版本>/plug-ins/`

2. 開啟Maya → **Windows > Settings/Preferences > Plug-in Manager**

3. 找到 `maya_mcp.py`，勾選 **Loaded** 和 **Auto load**

4. 在指令碼編輯器中確認：
   ```
   MayaMCP: 外掛程式已成功載入
   MayaMCP: 伺服器已啟動於 localhost:9877
   ```

### 3. 設定Claude Desktop

編輯設定檔（**Settings > Developer > Edit Config**）：

#### 方式A：使用npx（推薦）

**標準配置：**
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

**強制更新配置（每次啟動時拉取最新套件）：**
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
        "PYTHONPATH": "你的專案路徑/src",
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

> 💡 更多設定方式請查看 [`examples/`](examples/) 目錄

### 4. 測試連線

重新啟動Claude Desktop，然後詢問：

```
取得目前Maya場景資訊
```

如果看到場景資訊回傳，表示連線成功！✅

## 功能特性

### 🛠️ 核心工具

| 工具 | 功能 |
|-----|------|
| `get_scene_info` | 取得場景資訊（物件、相機、燈光） |
| `get_object_info` | 取得物件詳情（位置、旋轉、材質） |
| `create_primitive` | 建立幾何體（cube/sphere/cylinder/plane/torus） |
| `delete_object` | 刪除物件 |
| `transform_object` | 變換物件（移動/旋轉/縮放） |
| `set_material` | 設定材質和顏色 |
| `execute_maya_code` | 執行Python程式碼 |
| `smart_select` | 智慧物件選擇（支援正則與過濾） |
| `get_scene_summary` | 取得全面的場景摘要 |
| `get_console_output` | 取得Maya控制台/指令碼編輯器輸出 🆕 |

### 💬 範例對話

```
使用者：建立一個紅色的立方體，位置在(0, 5, 0)

Claude：
1. 建立了立方體
2. 移動到指定位置
3. 套用了紅色材質
✅ 完成
```

```
使用者：建立一個簡單的桌椅場景並擷取截圖

Claude：
1. 建立了桌面（縮放後的立方體）
2. 建立了4個桌腳（圓柱體）
3. 建立了椅子
4. 設定了材質
5. 擷取了視埠截圖
✅ [顯示截圖]
```

## 使用範例

### 基礎操作

```
# 場景查詢
"顯示目前場景的所有物件"
"取得pCube1的詳細資訊"
"取得控制台輸出查看最近的Maya日誌"

# 建立物件
"建立一個名為mySphere的球體"
"建立10個立方體排成一行"

# 修改物件
"將pCube1移動到(5, 0, 0)"
"將pSphere1設為藍色"
"將pCylinder1在Y軸旋轉45度"

# 智慧選擇
"選擇所有名稱包含'character'的物件"
"尋找所有面數超過5000的網格"
```

### 進階操作

```
# 程序化建模
"執行程式碼建立一個5x5的立方體網格"

# 頂點/面編輯
"建立一個平面並編輯頂點製作地形"
"擠出面來建立細節"

# UV編輯
"為選中物件套用自動UV投影"
"為球體建立球形UV對映"

# 動畫
"為彈跳球建立關鍵影格動畫"
"設定三點照明系統"

# 綁定
"建立包含5個關節的脊椎骨骼鏈"
"設定父約束"

# 動力學
"建立帶重力的粒子系統"
"為平面套用彎曲變形器"

# 布林運算
"從cube1中減去cube2"
"合併兩個重疊的球體"

# 批次操作
"為所有球體設定隨機顏色"

# 複雜場景
"建立一個簡單的室內場景，包含地板、牆壁和家具"
```

## 設定選項

### 環境變數

| 變數 | 預設值 | 說明 |
|------|--------|------|
| `MAYA_HOST` | `localhost` | Maya伺服器位址 |
| `MAYA_PORT` | `9877` | Maya伺服器連接埠 |
| `PYTHONPATH` | - | Python模組搜尋路徑（僅Python直接模式需要） |

### 自訂連接埠

**在Maya外掛中修改：**
```python
start_maya_mcp_server(host='localhost', port=9878)
```

**在設定檔中修改：**
```json
"env": {
  "MAYA_PORT": "9878"
}
```

## 疑難排解

### 連線失敗

**問題：** "無法連接至Maya"

**解決方案：**
1. ✅ 確認Maya正在執行
2. ✅ 確認外掛已載入（檢查外掛管理器）
3. ✅ 檢查指令碼編輯器中的啟動訊息
4. ✅ 確認連接埠9877未被佔用

### 模組未找到

**問題：** "ModuleNotFoundError: No module named 'maya_mcp'"

**解決方案：**
1. 安裝相依套件：`pip install "mcp[cli]>=1.3.0"`
2. 檢查PYTHONPATH設定（如使用Python直接模式）
3. 嘗試使用npx方式

### 外掛載入失敗

**問題：** Maya回報"No initializePlugin() function"

**解決方案：**
- 確保使用最新版本的 `maya_mcp.py`
- 外掛檔案包含 `initializePlugin()` 和 `uninitializePlugin()` 函式

## 安全注意事項

⚠️ **重要提示：**

- `execute_maya_code` 工具允許執行任意Python程式碼
- 始終在執行前**儲存Maya場景**
- 在生產環境中謹慎使用
- 建議先在測試場景中驗證操作

## 日誌

伺服器日誌儲存於：
- **Windows:** `%TEMP%\maya-mcp\maya-mcp.log`
- **macOS/Linux:** `/tmp/maya-mcp/maya-mcp.log`

查看日誌以偵錯連線問題或指令執行錯誤。

## 開發

### 新增工具

1. 在 `plug-ins/maya_mcp.py` 中新增指令處理器
2. 在 `src/maya_mcp/server.py` 中新增MCP工具定義
3. 測試新工具

### 執行開發伺服器

```bash
# 設定環境
set PYTHONPATH=d:/path/to/maya-mcp-server/src

# 執行伺服器
python -m maya_mcp.server
```

## 貢獻

歡迎貢獻！請查看 [`CONTRIBUTING.md`](CONTRIBUTING.md)

## 致謝

本專案受以下專案啟發：
- [Blender-MCP](https://github.com/ahujasid/blender-mcp) - 架構設計參考

## 授權

[MIT License](LICENSE)

## 免責聲明

這是一個第三方專案，非Autodesk官方產品。

---

<div align="center">

**[開始使用](examples/)** • **[設定指南](examples/README.md)** • **[問題回報](../../issues)**

為Maya藝術家和AI愛好者傾心打造 ❤️

</div>