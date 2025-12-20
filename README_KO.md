# Maya MCP Server

**Model Context Protocol을 통해 Claude AI를 Autodesk Maya에 연결**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Maya 2020+](https://img.shields.io/badge/maya-2020+-green.svg)](https://www.autodesk.com/products/maya/)

[English](README.md) | [简体中文](README_CN.md) | [繁體中文](README_CN_TW.md) | [日本語](README_JP.md) | [한국어](README_KO.md) | [Español](README_ES.md) | [Français](README_FR.md) | [Deutsch](README_DE.md) | [Русский](README_RU.md)

---

## 개요

Maya MCP Server는 Claude AI가 Model Context Protocol을 통해 Autodesk Maya를 직접 제어할 수 있게 합니다:

- 🎨 AI 지원 3D 모델링
- 🤖 자연어로 Maya 제어
- 📸 실시간 장면 미리보기
- 🔧 워크플로우 자동화

## 빠른 시작

### 1. 종속성 설치

```bash
pip install "mcp[cli]>=1.3.0"
```

### 2. Maya 플러그인 로드

Maya의 **플러그인 관리자**에서 `plug-ins/maya_mcp.py`를 로드합니다:

1. `plug-ins/maya_mcp.py`를 다음 위치에 복사:
   - Windows: `C:\Users\<사용자명>\Documents\maya\<버전>\plug-ins\`
   - macOS: `~/maya/<버전>/plug-ins/`

2. Maya 열기 → **Windows > Settings/Preferences > Plug-in Manager**

3. `maya_mcp.py`를 찾아 **Loaded**와 **Auto load**에 체크

4. 스크립트 편집기에서 확인:
   ```
   MayaMCP: 플러그인이 성공적으로 로드되었습니다
   MayaMCP: 서버가 localhost:9877에서 시작되었습니다
   ```

### 3. Claude Desktop 구성

구성 파일 편집(**Settings > Developer > Edit Config**):

#### 방법 A: npx 사용 (권장)

**표준 구성:**
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

**강제 업데이트 구성 (시작할 때마다 최신 패키지 가져오기):**
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

#### 방법 B: Python 사용

```json
{
  "mcpServers": {
    "maya-mcp": {
      "command": "python",
      "args": ["-m", "maya_mcp.server"],
      "env": {
        "PYTHONPATH": "프로젝트경로/src",
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

> 💡 더 많은 구성 방법은 [`examples/`](examples/) 디렉토리 참조

### 4. 연결 테스트

Claude Desktop을 재시작하고 다음과 같이 질문:

```
현재 Maya 장면 정보 가져오기
```

장면 정보가 반환되면 연결 성공입니다! ✅

## 기능

### 🛠️ 핵심 도구

| 도구 | 기능 |
|-----|------|
| `get_scene_info` | 장면 정보 가져오기 (객체, 카메라, 조명) |
| `get_object_info` | 객체 세부정보 가져오기 (위치, 회전, 재질) |
| `create_primitive` | 지오메트리 생성 (cube/sphere/cylinder/plane/torus) |
| `delete_object` | 객체 삭제 |
| `transform_object` | 객체 변환 (이동/회전/스케일) |
| `set_material` | 재질 및 색상 설정 |
| `execute_maya_code` | Python 코드 실행 |
| `smart_select` | 스마트 객체 선택 (정규식 및 필터 지원) |
| `get_scene_summary` | 포괄적인 장면 요약 가져오기 |
| `get_console_output` | Maya 콘솔/스크립트 편집기 출력 가져오기 🆕 |

### 💬 대화 예시

```
사용자: (0, 5, 0) 위치에 빨간 큐브 생성해줘

Claude:
1. 큐브를 생성했습니다
2. 지정된 위치로 이동했습니다
3. 빨간색 재질을 적용했습니다
✅ 완료
```

```
사용자: 간단한 테이블과 의자 장면을 만들고 스크린샷 찍어줘

Claude:
1. 테이블 상판(스케일된 큐브) 생성
2. 테이블 다리 4개(실린더) 생성
3. 의자 생성
4. 재질 설정
5. 뷰포트 스크린샷 캡처
✅ [스크린샷 표시]
```

## 사용 예제

### 기본 작업

```
# 장면 쿼리
"현재 장면의 모든 객체 표시"
"pCube1의 상세 정보 가져오기"
"콘솔 출력을 가져와 최근 Maya 로그 확인"

# 객체 생성
"mySphere라는 이름의 구체 생성"
"10개의 큐브를 한 줄로 생성"

# 객체 수정
"pCube1을 (5, 0, 0)으로 이동"
"pSphere1을 파란색으로 설정"
"pCylinder1을 Y축으로 45도 회전"

# 스마트 선택
"이름에 'character'가 포함된 모든 객체 선택"
"5000면 이상의 모든 메쉬 찾기"
```

### 고급 작업

```
# 절차적 모델링
"5x5 큐브 그리드를 생성하는 코드 실행"

# 버텍스/면 편집
"평면을 만들고 버텍스를 편집하여 지형 생성"
"면을 돌출하여 디테일 생성"

# UV 편집
"선택한 객체에 자동 UV 투영 적용"
"구체에 구면 UV 매핑 생성"

# 애니메이션
"튀는 공의 키프레임 애니메이션 생성"
"3점 조명 시스템 설정"

# 리깅
"5개의 조인트를 가진 척추 본 체인 생성"
"부모 컨스트레인트 설정"

# 다이나믹스
"중력이 있는 파티클 시스템 생성"
"평면에 벤드 디포머 적용"

# 불리언 연산
"cube1에서 cube2 빼기"
"겹치는 두 구체 결합"

# 일괄 작업
"모든 구체에 무작위 색상 설정"

# 복잡한 장면
"바닥, 벽, 가구를 포함한 간단한 실내 장면 생성"
```

## 구성 옵션

### 환경 변수

| 변수 | 기본값 | 설명 |
|------|--------|------|
| `MAYA_HOST` | `localhost` | Maya 서버 주소 |
| `MAYA_PORT` | `9877` | Maya 서버 포트 |
| `PYTHONPATH` | - | Python 모듈 검색 경로 (Python 직접 모드만 필요) |

### 사용자 정의 포트

**Maya 플러그인에서 수정:**
```python
start_maya_mcp_server(host='localhost', port=9878)
```

**구성 파일에서 수정:**
```json
"env": {
  "MAYA_PORT": "9878"
}
```

## 문제 해결

### 연결 실패

**문제:** "Maya에 연결할 수 없습니다"

**해결책:**
1. ✅ Maya가 실행 중인지 확인
2. ✅ 플러그인이 로드되었는지 확인 (플러그인 관리자 확인)
3. ✅ 스크립트 편집기에서 시작 메시지 확인
4. ✅ 포트 9877이 사용 중이지 않은지 확인

### 모듈을 찾을 수 없음

**문제:** "ModuleNotFoundError: No module named 'maya_mcp'"

**해결책:**
1. 종속성 설치: `pip install "mcp[cli]>=1.3.0"`
2. PYTHONPATH 설정 확인 (Python 직접 모드 사용 시)
3. npx 방식 시도

### 플러그인 로드 실패

**문제:** Maya가 "No initializePlugin() function" 보고

**해결책:**
- 최신 버전의 `maya_mcp.py` 사용 확인
- 플러그인 파일에 `initializePlugin()` 및 `uninitializePlugin()` 함수 포함 확인

## 보안 주의사항

⚠️ **중요 참고:**

- `execute_maya_code` 도구는 임의의 Python 코드 실행을 허용합니다
- 실행 전에 항상 **Maya 장면을 저장**하세요
- 프로덕션 환경에서는 신중하게 사용하세요
- 테스트 장면에서 작업을 먼저 검증하는 것이 좋습니다

## 로그

서버 로그는 다음 위치에 저장됩니다:
- **Windows:** `%TEMP%\maya-mcp\maya-mcp.log`
- **macOS/Linux:** `/tmp/maya-mcp/maya-mcp.log`

연결 문제나 명령 실행 오류를 디버그하려면 로그를 확인하세요.

## 개발

### 새 도구 추가

1. `plug-ins/maya_mcp.py`에 명령 핸들러 추가
2. `src/maya_mcp/server.py`에 MCP 도구 정의 추가
3. 새 도구 테스트

### 개발 서버 실행

```bash
# 환경 설정
set PYTHONPATH=d:/path/to/maya-mcp-server/src

# 서버 실행
python -m maya_mcp.server
```

## 기여

기여를 환영합니다! 자세한 내용은 [`CONTRIBUTING.md`](CONTRIBUTING.md)를 참조하세요.

## 감사의 말

이 프로젝트는 다음 프로젝트에서 영감을 받았습니다:
- [Blender-MCP](https://github.com/ahujasid/blender-mcp) - 아키텍처 설계 참조

## 라이선스

[MIT License](LICENSE)

## 면책 조항

이것은 타사 프로젝트이며 Autodesk 공식 제품이 아닙니다.

---

<div align="center">

**[시작하기](examples/)** • **[구성 가이드](examples/README.md)** • **[문제 보고](../../issues)**

Maya 아티스트와 AI 애호가를 위해 만들어졌습니다 ❤️

</div>