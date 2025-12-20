# Maya MCP Server

**Connectez Claude AI à Autodesk Maya via Model Context Protocol**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Maya 2020+](https://img.shields.io/badge/maya-2020+-green.svg)](https://www.autodesk.com/products/maya/)

[English](README.md) | [简体中文](README_CN.md) | [繁體中文](README_CN_TW.md) | [日本語](README_JP.md) | [한국어](README_KO.md) | [Español](README_ES.md) | [Français](README_FR.md) | [Deutsch](README_DE.md) | [Русский](README_RU.md)

---

## Vue d'ensemble

Maya MCP Server permet à Claude AI de contrôler directement Autodesk Maya via Model Context Protocol, permettant :

- 🎨 Modélisation 3D assistée par IA
- 🤖 Contrôle de Maya en langage naturel
- 📸 Aperçu de scène en temps réel
- 🔧 Automatisation du flux de travail

## Démarrage Rapide

### 1. Installer les Dépendances

```bash
pip install "mcp[cli]>=1.3.0"
```

### 2. Charger le Plugin Maya

Chargez `plug-ins/maya_mcp.py` dans le **Gestionnaire de Plugins** de Maya :

1. Copiez `plug-ins/maya_mcp.py` vers :
   - Windows : `C:\Users\<nom_utilisateur>\Documents\maya\<version>\plug-ins\`
   - macOS : `~/maya/<version>/plug-ins/`

2. Ouvrez Maya → **Windows > Settings/Preferences > Plug-in Manager**

3. Trouvez `maya_mcp.py`, cochez **Loaded** et **Auto load**

4. Vérifiez dans l'Éditeur de Scripts :
   ```
   MayaMCP: Plugin chargé avec succès
   MayaMCP: Serveur démarré sur localhost:9877
   ```

### 3. Configurer Claude Desktop

Éditez le fichier de configuration (**Settings > Developer > Edit Config**) :

#### Méthode A : Utilisation de npx (Recommandé)

**Configuration standard :**
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

**Configuration de mise à jour forcée (toujours télécharger le dernier paquet) :**
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

#### Méthode B : Utilisation de Python

```json
{
  "mcpServers": {
    "maya-mcp": {
      "command": "python",
      "args": ["-m", "maya_mcp.server"],
      "env": {
        "PYTHONPATH": "chemin_du_projet/src",
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

> 💡 Consultez le répertoire [`examples/`](examples/) pour d'autres méthodes de configuration

### 4. Tester la Connexion

Redémarrez Claude Desktop et demandez :

```
Obtenir les informations de la scène Maya actuelle
```

Si vous voyez les informations de la scène, la connexion est réussie ! ✅

## Fonctionnalités

### 🛠️ Outils Principaux

| Outil | Fonction |
|-----|------|
| `get_scene_info` | Obtenir les informations de la scène (objets, caméras, lumières) |
| `get_object_info` | Obtenir les détails de l'objet (position, rotation, matériau) |
| `create_primitive` | Créer une géométrie (cube/sphere/cylinder/plane/torus) |
| `delete_object` | Supprimer un objet |
| `transform_object` | Transformer un objet (déplacer/pivoter/échelle) |
| `set_material` | Définir le matériau et la couleur |
| `execute_maya_code` | Exécuter du code Python |
| `smart_select` | Sélection intelligente d'objets avec regex et filtres |
| `get_scene_summary` | Obtenir un résumé complet de la scène |
| `get_console_output` | Obtenir la sortie de la console/éditeur de scripts Maya 🆕 |

### 💬 Exemples de Conversation

```
Utilisateur : Crée un cube rouge à la position (0, 5, 0)

Claude :
1. J'ai créé le cube
2. Je l'ai déplacé à la position spécifiée
3. J'ai appliqué le matériau rouge
✅ Terminé
```

```
Utilisateur : Crée une scène simple de table et chaise

Claude :
1. J'ai créé le plateau de table (cube mis à l'échelle)
2. J'ai créé 4 pieds de table (cylindres)
3. J'ai créé la chaise
4. J'ai défini les matériaux
✅ Scène créée avec succès
```

## Exemples d'Utilisation

### Opérations de Base

```
# Requêtes de scène
"Afficher tous les objets dans la scène actuelle"
"Obtenir les informations détaillées de pCube1"
"Obtenir la sortie de la console pour voir les journaux récents de Maya"

# Créer des objets
"Créer une sphère nommée mySphere"
"Créer 10 cubes en ligne"

# Modifier des objets
"Déplacer pCube1 vers (5, 0, 0)"
"Définir pSphere1 en bleu"
"Faire pivoter pCylinder1 de 45 degrés sur l'axe Y"

# Sélection intelligente
"Sélectionner tous les objets avec 'character' dans leur nom"
"Trouver tous les maillages avec plus de 5000 faces"
```

### Opérations Avancées

```
# Modélisation procédurale
"Exécuter du code pour créer une grille de cubes 5x5"

# Édition de sommets/faces
"Créer un plan et éditer les sommets pour faire un terrain"
"Extruder des faces pour créer des détails"

# Édition UV
"Appliquer une projection UV automatique aux objets sélectionnés"
"Créer un mappage UV sphérique pour la sphère"

# Animation
"Créer une animation par images clés pour une balle rebondissante"
"Configurer un système d'éclairage à 3 points"

# Rigging
"Créer une chaîne d'os de colonne vertébrale avec 5 articulations"
"Configurer des contraintes de parent"

# Dynamique
"Créer un système de particules avec gravité"
"Appliquer un déformateur de courbure au plan"

# Opérations booléennes
"Soustraire cube2 de cube1"
"Unir deux sphères qui se chevauchent"

# Opérations par lots
"Définir des couleurs aléatoires pour toutes les sphères"

# Scènes complexes
"Créer une scène intérieure simple avec sol, murs et meubles"
```

## Options de Configuration

### Variables d'Environnement

| Variable | Valeur par Défaut | Description |
|------|--------|------|
| `MAYA_HOST` | `localhost` | Adresse du serveur Maya |
| `MAYA_PORT` | `9877` | Port du serveur Maya |
| `PYTHONPATH` | - | Chemin de recherche des modules Python (uniquement pour le mode Python direct) |

### Port Personnalisé

**Modifier dans le plugin Maya :**
```python
start_maya_mcp_server(host='localhost', port=9878)
```

**Modifier dans le fichier de configuration :**
```json
"env": {
  "MAYA_PORT": "9878"
}
```

## Dépannage

### Échec de Connexion

**Problème :** "Impossible de se connecter à Maya"

**Solution :**
1. ✅ Confirmez que Maya est en cours d'exécution
2. ✅ Confirmez que le plugin est chargé (vérifiez le Gestionnaire de Plugins)
3. ✅ Vérifiez le message de démarrage dans l'Éditeur de Scripts
4. ✅ Confirmez que le port 9877 n'est pas utilisé

### Module Non Trouvé

**Problème :** "ModuleNotFoundError: No module named 'maya_mcp'"

**Solution :**
1. Installez les dépendances : `pip install "mcp[cli]>=1.3.0"`
2. Vérifiez la configuration de PYTHONPATH (si vous utilisez le mode Python direct)
3. Essayez d'utiliser la méthode npx

### Échec du Chargement du Plugin

**Problème :** Maya signale "No initializePlugin() function"

**Solution :**
- Assurez-vous d'utiliser la dernière version de `maya_mcp.py`
- Le fichier du plugin doit contenir les fonctions `initializePlugin()` et `uninitializePlugin()`

## Avis de Sécurité

⚠️ **Note Importante :**

- L'outil `execute_maya_code` permet l'exécution de code Python arbitraire
- Toujours **sauvegarder votre scène Maya** avant l'exécution
- Utilisez avec précaution dans les environnements de production
- Il est recommandé de vérifier d'abord les opérations dans des scènes de test

## Journaux

Les journaux du serveur sont enregistrés dans :
- **Windows :** `%TEMP%\maya-mcp\maya-mcp.log`
- **macOS/Linux :** `/tmp/maya-mcp/maya-mcp.log`

Consultez les journaux pour déboguer les problèmes de connexion ou les erreurs d'exécution de commandes.

## Développement

### Ajouter de Nouveaux Outils

1. Ajoutez le gestionnaire de commandes dans `plug-ins/maya_mcp.py`
2. Ajoutez la définition de l'outil MCP dans `src/maya_mcp/server.py`
3. Testez le nouvel outil

### Exécuter le Serveur de Développement

```bash
# Configurer l'environnement
export PYTHONPATH=/path/to/maya-mcp-server/src

# Exécuter le serveur
python -m maya_mcp.server
```

## Contributions

Les contributions sont les bienvenues ! Consultez [`CONTRIBUTING.md`](CONTRIBUTING.md)

## Remerciements

Ce projet s'inspire de :
- [Blender-MCP](https://github.com/ahujasid/blender-mcp) - Référence de conception d'architecture

## Licence

[MIT License](LICENSE)

## Clause de Non-Responsabilité

Ceci est un projet tiers, pas un produit officiel d'Autodesk.

---

<div align="center">

**[Commencer](examples/)** • **[Guide de Configuration](examples/README.md)** • **[Signaler un Problème](../../issues)**

Fait avec ❤️ pour les artistes Maya et les passionnés d'IA

</div>