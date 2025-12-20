# Maya MCP Server

**Verbinden Sie Claude AI mit Autodesk Maya über Model Context Protocol**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Maya 2020+](https://img.shields.io/badge/maya-2020+-green.svg)](https://www.autodesk.com/products/maya/)

[English](README.md) | [简体中文](README_CN.md) | [繁體中文](README_CN_TW.md) | [日本語](README_JP.md) | [한국어](README_KO.md) | [Español](README_ES.md) | [Français](README_FR.md) | [Deutsch](README_DE.md) | [Русский](README_RU.md)

---

## Überblick

Maya MCP Server ermöglicht es Claude AI, Autodesk Maya direkt über das Model Context Protocol zu steuern und bietet:

- 🎨 KI-gestützte 3D-Modellierung
- 🤖 Steuerung von Maya in natürlicher Sprache
- 📸 Echtzeit-Szenenvorschau
- 🔧 Workflow-Automatisierung

## Schnellstart

### 1. Abhängigkeiten Installieren

```bash
pip install "mcp[cli]>=1.3.0"
```

### 2. Maya-Plugin Laden

Laden Sie `plug-ins/maya_mcp.py` im **Plugin-Manager** von Maya:

1. Kopieren Sie `plug-ins/maya_mcp.py` nach:
   - Windows: `C:\Users\<Benutzername>\Documents\maya\<Version>\plug-ins\`
   - macOS: `~/maya/<Version>/plug-ins/`

2. Öffnen Sie Maya → **Windows > Settings/Preferences > Plug-in Manager**

3. Finden Sie `maya_mcp.py`, aktivieren Sie **Loaded** und **Auto load**

4. Überprüfen Sie im Script-Editor:
   ```
   MayaMCP: Plugin erfolgreich geladen
   MayaMCP: Server gestartet auf localhost:9877
   ```

### 3. Claude Desktop Konfigurieren

Bearbeiten Sie die Konfigurationsdatei (**Settings > Developer > Edit Config**):

#### Methode A: Mit npx (Empfohlen)

```json
{
  "mcpServers": {
    "maya-mcp": {
      "command": "npx",
      "args": [
        "--yes",
        "--package=Ihr_Projektpfad",
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

#### Methode B: Mit Python

```json
{
  "mcpServers": {
    "maya-mcp": {
      "command": "python",
      "args": ["-m", "maya_mcp.server"],
      "env": {
        "PYTHONPATH": "Ihr_Projektpfad/src",
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

> 💡 Weitere Konfigurationsmethoden finden Sie im Verzeichnis [`examples/`](examples/)

### 4. Verbindung Testen

Starten Sie Claude Desktop neu und fragen Sie:

```
Aktuelle Maya-Szeneninformationen abrufen
```

Wenn Sie die Szeneninformationen sehen, war die Verbindung erfolgreich! ✅

## Funktionen

### 🛠️ Hauptwerkzeuge

| Werkzeug | Funktion |
|-----|------|
| `get_scene_info` | Szeneninformationen abrufen (Objekte, Kameras, Lichter) |
| `get_object_info` | Objektdetails abrufen (Position, Rotation, Material) |
| `create_primitive` | Geometrie erstellen (cube/sphere/cylinder/plane/torus) |
| `delete_object` | Objekt löschen |
| `transform_object` | Objekt transformieren (verschieben/drehen/skalieren) |
| `set_material` | Material und Farbe festlegen |
| `execute_maya_code` | Python-Code ausführen |
| `get_viewport_screenshot` | Viewport-Screenshot erfassen ⚠️ |
| `smart_select` | Intelligente Objektauswahl mit Regex und Filtern |
| `get_scene_summary` | Umfassende Szenenzusammenfassung abrufen |
| `get_console_output` | Maya-Konsole/Script-Editor-Ausgabe abrufen 🆕 |

> ⚠️ Hinweis: `get_viewport_screenshot` kann in einigen Maya-Versionen aufgrund von Playblast-Kompatibilitätsproblemen instabil sein.

### 💬 Gesprächsbeispiele

```
Benutzer: Erstelle einen roten Würfel an Position (0, 5, 0)

Claude:
1. Würfel erstellt
2. An die angegebene Position verschoben
3. Rotes Material angewendet
✅ Abgeschlossen
```

```
Benutzer: Erstelle eine einfache Tisch- und Stuhlszene und mache einen Screenshot

Claude:
1. Tischplatte erstellt (skalierter Würfel)
2. 4 Tischbeine erstellt (Zylinder)
3. Stuhl erstellt
4. Materialien festgelegt
5. Viewport-Screenshot erfasst
✅ [Screenshot anzeigen]
```

## Verwendungsbeispiele

### Grundlegende Operationen

```
# Szenenabfragen
"Alle Objekte in der aktuellen Szene anzeigen"
"Detaillierte Informationen zu pCube1 abrufen"
"Konsolenausgabe abrufen, um aktuelle Maya-Logs zu sehen"

# Objekte erstellen
"Eine Kugel namens mySphere erstellen"
"10 Würfel in einer Reihe erstellen"

# Objekte ändern
"pCube1 nach (5, 0, 0) verschieben"
"pSphere1 auf Blau setzen"
"pCylinder1 um 45 Grad um die Y-Achse drehen"

# Intelligente Auswahl
"Alle Objekte mit 'character' im Namen auswählen"
"Alle Meshes mit mehr als 5000 Flächen finden"
```

### Erweiterte Operationen

```
# Prozedurale Modellierung
"Code ausführen, um ein 5x5-Würfelgitter zu erstellen"

# Vertex/Flächen-Bearbeitung
"Eine Ebene erstellen und Vertices bearbeiten, um ein Gelände zu erstellen"
"Flächen extrudieren, um Details zu erstellen"

# UV-Bearbeitung
"Automatische UV-Projektion auf ausgewählte Objekte anwenden"
"Sphärisches UV-Mapping für die Kugel erstellen"

# Animation
"Keyframe-Animation für hüpfenden Ball erstellen"
"3-Punkt-Beleuchtungssystem einrichten"

# Rigging
"Wirbelsäulen-Knochenkette mit 5 Gelenken erstellen"
"Parent-Constraints einrichten"

# Dynamik
"Partikelsystem mit Schwerkraft erstellen"
"Bend-Deformer auf Ebene anwenden"

# Boolesche Operationen
"cube2 von cube1 subtrahieren"
"Zwei überlappende Kugeln vereinen"

# Stapeloperationen
"Zufällige Farben für alle Kugeln festlegen"

# Komplexe Szenen
"Eine einfache Innenszene mit Boden, Wänden und Möbeln erstellen"
```

## Konfigurationsoptionen

### Umgebungsvariablen

| Variable | Standardwert | Beschreibung |
|------|--------|------|
| `MAYA_HOST` | `localhost` | Maya-Serveradresse |
| `MAYA_PORT` | `9877` | Maya-Serverport |
| `PYTHONPATH` | - | Python-Modulsuchpfad (nur für direkten Python-Modus erforderlich) |

### Benutzerdefinierter Port

**Im Maya-Plugin ändern:**
```python
start_maya_mcp_server(host='localhost', port=9878)
```

**In der Konfigurationsdatei ändern:**
```json
"env": {
  "MAYA_PORT": "9878"
}
```

## Fehlerbehebung

### Verbindungsfehler

**Problem:** "Verbindung zu Maya nicht möglich"

**Lösung:**
1. ✅ Bestätigen Sie, dass Maya läuft
2. ✅ Bestätigen Sie, dass das Plugin geladen ist (Plugin-Manager überprüfen)
3. ✅ Startmeldung im Script-Editor überprüfen
4. ✅ Bestätigen Sie, dass Port 9877 nicht verwendet wird

### Modul Nicht Gefunden

**Problem:** "ModuleNotFoundError: No module named 'maya_mcp'"

**Lösung:**
1. Abhängigkeiten installieren: `pip install "mcp[cli]>=1.3.0"`
2. PYTHONPATH-Konfiguration überprüfen (bei direktem Python-Modus)
3. npx-Methode versuchen

### Plugin-Ladefehler

**Problem:** Maya meldet "No initializePlugin() function"

**Lösung:**
- Stellen Sie sicher, dass Sie die neueste Version von `maya_mcp.py` verwenden
- Die Plugin-Datei muss die Funktionen `initializePlugin()` und `uninitializePlugin()` enthalten

## Sicherheitshinweise

⚠️ **Wichtiger Hinweis:**

- Das Werkzeug `execute_maya_code` ermöglicht die Ausführung von beliebigem Python-Code
- **Speichern Sie immer Ihre Maya-Szene** vor der Ausführung
- Vorsicht bei der Verwendung in Produktionsumgebungen
- Es wird empfohlen, Operationen zuerst in Testszenen zu verifizieren

## Protokolle

Server-Protokolle werden gespeichert in:
- **Windows:** `%TEMP%\maya-mcp\maya-mcp.log`
- **macOS/Linux:** `/tmp/maya-mcp/maya-mcp.log`

Überprüfen Sie die Protokolle, um Verbindungsprobleme oder Befehlsausführungsfehler zu debuggen.

## Entwicklung

### Neue Werkzeuge Hinzufügen

1. Befehlshandler in `plug-ins/maya_mcp.py` hinzufügen
2. MCP-Werkzeugdefinition in `src/maya_mcp/server.py` hinzufügen
3. Neues Werkzeug testen

### Entwicklungsserver Ausführen

```bash
# Umgebung einrichten
export PYTHONPATH=/path/to/maya-mcp-server/src

# Server ausführen
python -m maya_mcp.server
```

## Beiträge

Beiträge sind willkommen! Siehe [`CONTRIBUTING.md`](CONTRIBUTING.md)

## Danksagungen

Dieses Projekt wurde inspiriert von:
- [Blender-MCP](https://github.com/ahujasid/blender-mcp) - Architekturdesign-Referenz

## Lizenz

[MIT License](LICENSE)

## Haftungsausschluss

Dies ist ein Drittanbieterprojekt, kein offizielles Autodesk-Produkt.

---

<div align="center">

**[Erste Schritte](examples/)** • **[Konfigurationsanleitung](examples/README.md)** • **[Problem Melden](../../issues)**

Mit ❤️ für Maya-Künstler und KI-Enthusiasten erstellt

</div>