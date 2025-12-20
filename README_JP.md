# Maya MCP Server

**Model Context ProtocolによってClaude AIをAutodesk Mayaに接続**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Maya 2020+](https://img.shields.io/badge/maya-2020+-green.svg)](https://www.autodesk.com/products/maya/)

[English](README.md) | [简体中文](README_CN.md) | [繁體中文](README_CN_TW.md) | [日本語](README_JP.md) | [한국어](README_KO.md) | [Español](README_ES.md) | [Français](README_FR.md) | [Deutsch](README_DE.md) | [Русский](README_RU.md)

---

## 概要

Maya MCP ServerはClaude AIがModel Context Protocolを通じてAutodesk Mayaを直接制御できるようにします：

- 🎨 AI支援3Dモデリング
- 🤖 自然言語でMayaを制御
- 📸 リアルタイムシーンプレビュー
- 🔧 ワークフロー自動化

## クイックスタート

### 1. 依存関係のインストール

```bash
pip install "mcp[cli]>=1.3.0"
```

### 2. Mayaプラグインの読み込み

Mayaの**プラグインマネージャー**で `plug-ins/maya_mcp.py` を読み込みます：

1. `plug-ins/maya_mcp.py` を以下にコピー：
   - Windows: `C:\Users\<ユーザー名>\Documents\maya\<バージョン>\plug-ins\`
   - macOS: `~/maya/<バージョン>/plug-ins/`

2. Mayaを開く → **Windows > Settings/Preferences > Plug-in Manager**

3. `maya_mcp.py` を見つけ、**Loaded** と **Auto load** にチェック

4. スクリプトエディタで確認：
   ```
   MayaMCP: プラグインが正常に読み込まれました
   MayaMCP: サーバーが localhost:9877 で起動しました
   ```

### 3. Claude Desktopの設定

設定ファイルを編集（**Settings > Developer > Edit Config**）：

#### 方法A：npxを使用（推奨）

```json
{
  "mcpServers": {
    "maya-mcp": {
      "command": "npx",
      "args": [
        "--yes",
        "--package=プロジェクトパス",
        "maya-mcp"
      ],
      "env": {
        "MAYA_HOST": "localhost",
        "MAYA_PORT": "9877"
      },
      "alwaysAllow": [
          "get_scene_info",
          "create_primitive",
          "delete_object",
          "set_material",
          "get_viewport_screenshot",
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

#### 方法B：Pythonを使用

```json
{
  "mcpServers": {
    "maya-mcp": {
      "command": "python",
      "args": ["-m", "maya_mcp.server"],
      "env": {
        "PYTHONPATH": "プロジェクトパス/src",
        "MAYA_HOST": "localhost",
        "MAYA_PORT": "9877"
      },
      "alwaysAllow": [
          "get_scene_info",
          "create_primitive",
          "delete_object",
          "set_material",
          "get_viewport_screenshot",
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

> 💡 その他の設定方法は [`examples/`](examples/) ディレクトリを参照

### 4. 接続テスト

Claude Desktopを再起動し、次のように質問：

```
現在のMayaシーン情報を取得
```

シーン情報が返されたら、接続成功です！✅

## 機能

### 🛠️ コアツール

| ツール | 機能 |
|-----|------|
| `get_scene_info` | シーン情報を取得（オブジェクト、カメラ、ライト） |
| `get_object_info` | オブジェクト詳細を取得（位置、回転、マテリアル） |
| `create_primitive` | ジオメトリを作成（cube/sphere/cylinder/plane/torus） |
| `delete_object` | オブジェクトを削除 |
| `transform_object` | オブジェクトを変換（移動/回転/スケール） |
| `set_material` | マテリアルと色を設定 |
| `execute_maya_code` | Pythonコードを実行 |
| `get_viewport_screenshot` | ビューポートのスクリーンショットをキャプチャ ⚠️ |
| `smart_select` | スマートオブジェクト選択（正規表現とフィルタ対応） |
| `get_scene_summary` | 包括的なシーン概要を取得 |
| `get_console_output` | Mayaコンソール/スクリプトエディタ出力を取得 🆕 |

> ⚠️ 注意：`get_viewport_screenshot`は、playblastの互換性問題により一部のMayaバージョンで不安定な場合があります。

### 💬 対話例

```
ユーザー：赤い立方体を(0, 5, 0)の位置に作成して

Claude：
1. 立方体を作成しました
2. 指定位置に移動しました
3. 赤いマテリアルを適用しました
✅ 完了
```

```
ユーザー：シンプルなテーブルと椅子のシーンを作成してスクリーンショットを撮って

Claude：
1. テーブルトップ（スケールした立方体）を作成
2. 4本のテーブル脚（円柱）を作成
3. 椅子を作成
4. マテリアルを設定
5. ビューポートのスクリーンショットをキャプチャ
✅ [スクリーンショットを表示]
```

## 使用例

### 基本操作

```
# シーンクエリ
"現在のシーンのすべてのオブジェクトを表示"
"pCube1の詳細情報を取得"
"コンソール出力を取得して最近のMayaログを確認"

# オブジェクト作成
"mySphereという名前の球体を作成"
"10個の立方体を一列に並べて作成"

# オブジェクト修正
"pCube1を(5, 0, 0)に移動"
"pSphere1を青色に設定"
"pCylinder1をY軸で45度回転"

# スマート選択
"名前に'character'を含むすべてのオブジェクトを選択"
"5000面以上のすべてのメッシュを検索"
```

### 高度な操作

```
# プロシージャルモデリング
"5x5の立方体グリッドを作成するコードを実行"

# 頂点/面編集
"プレーンを作成し、頂点を編集して地形を作成"
"面を押し出してディテールを作成"

# UV編集
"選択したオブジェクトに自動UV投影を適用"
"球体に球面UVマッピングを作成"

# アニメーション
"バウンスボールのキーフレームアニメーションを作成"
"3点照明システムをセットアップ"

# リギング
"5つのジョイントを持つ脊椎ボーンチェーンを作成"
"親コンストレイントをセットアップ"

# ダイナミクス
"重力付きのパーティクルシステムを作成"
"プレーンにベンドデフォーマを適用"

# ブール演算
"cube1からcube2を減算"
"2つの重なった球体を結合"

# バッチ操作
"すべての球体にランダムな色を設定"

# 複雑なシーン
"床、壁、家具を含むシンプルな室内シーンを作成"
```

## 設定オプション

### 環境変数

| 変数 | デフォルト値 | 説明 |
|------|------------|------|
| `MAYA_HOST` | `localhost` | Mayaサーバーアドレス |
| `MAYA_PORT` | `9877` | Mayaサーバーポート |
| `PYTHONPATH` | - | Pythonモジュール検索パス（Python直接モードのみ必要） |

### カスタムポート

**Mayaプラグインで変更：**
```python
start_maya_mcp_server(host='localhost', port=9878)
```

**設定ファイルで変更：**
```json
"env": {
  "MAYA_PORT": "9878"
}
```

## トラブルシューティング

### 接続失敗

**問題：** "Mayaに接続できません"

**解決策：**
1. ✅ Mayaが実行中であることを確認
2. ✅ プラグインが読み込まれていることを確認（プラグインマネージャーを確認）
3. ✅ スクリプトエディタで起動メッセージを確認
4. ✅ ポート9877が使用されていないことを確認

### モジュールが見つからない

**問題：** "ModuleNotFoundError: No module named 'maya_mcp'"

**解決策：**
1. 依存関係をインストール：`pip install "mcp[cli]>=1.3.0"`
2. PYTHONPATH設定を確認（Python直接モードを使用する場合）
3. npx方式を試す

### プラグイン読み込み失敗

**問題：** Mayaが "No initializePlugin() function" とレポート

**解決策：**
- 最新バージョンの `maya_mcp.py` を使用していることを確認
- プラグインファイルに `initializePlugin()` と `uninitializePlugin()` 関数が含まれていることを確認

## セキュリティに関する注意事項

⚠️ **重要な注意：**

- `execute_maya_code` ツールは任意のPythonコードの実行を許可します
- 実行前に必ず**Mayaシーンを保存**してください
- 本番環境では慎重に使用してください
- テストシーンで操作を検証することをお勧めします

## ログ

サーバーログは以下に保存されます：
- **Windows:** `%TEMP%\maya-mcp\maya-mcp.log`
- **macOS/Linux:** `/tmp/maya-mcp/maya-mcp.log`

接続問題やコマンド実行エラーをデバッグするためにログを確認してください。

## 開発

### 新しいツールの追加

1. `plug-ins/maya_mcp.py` にコマンドハンドラーを追加
2. `src/maya_mcp/server.py` にMCPツール定義を追加
3. 新しいツールをテスト

### 開発サーバーの実行

```bash
# 環境を設定
set PYTHONPATH=d:/path/to/maya-mcp-server/src

# サーバーを実行
python -m maya_mcp.server
```

## コントリビューション

コントリビューションを歓迎します！詳細は [`CONTRIBUTING.md`](CONTRIBUTING.md) を参照してください。

## 謝辞

このプロジェクトは以下のプロジェクトからインスピレーションを受けています：
- [Blender-MCP](https://github.com/ahujasid/blender-mcp) - アーキテクチャ設計の参考

## ライセンス

[MIT License](LICENSE)

## 免責事項

これはサードパーティプロジェクトであり、Autodesk公式製品ではありません。

---

<div align="center">

**[使い始める](examples/)** • **[設定ガイド](examples/README.md)** • **[問題報告](../../issues)**

Mayaアーティストとai愛好家のために心を込めて作成 ❤️

</div>