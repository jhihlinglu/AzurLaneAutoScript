# AzurLaneAutoScript (Alas)

> 碧藍航線全自動腳本 ✦ Full-auto Azur Lane bot ✦ 碧ブレイン全自動スクリプト ✦ 벽람항로 자동화 봇

**語言 / Language / 言語 / 언어**
[繁體中文](#繁體中文) ✦ [English](#english) ✦ [日本語](#日本語) ✦ [한국어](#한국어)

---

## 繁體中文

Alas 是一個帶有網頁介面的碧藍航線自動化腳本，支援國服、國際服、日服、台服。設計目標為 24 小時持續運行，可接手幾乎所有遊戲內容。

原始專案：[LmeSzinc/AzurLaneAutoScript](https://github.com/LmeSzinc/AzurLaneAutoScript)
本 Fork 額外支援 **Apple Silicon（ARM）Mac**。

### 主要功能

- 出擊：主線圖、活動圖、共鬥活動、緊急委託刷鑽石
- 收穫：委託、戰術學院、科研、後宅、大艦隊、每日抽卡
- 每日：每日任務、困難圖、演習、潛艇圖
- 大世界：餘燼信標、每月開荒、隱秘海域、深淵海域、賽壬要塞

### 安裝教學（Apple Silicon Mac）

> 適用 M1 / M2 / M3 / M4，macOS 12 以上

**第一步：安裝必要工具**

開啟「終端機」，貼上以下指令逐行執行：

```bash
# 安裝 Homebrew（套件管理器）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 安裝 miniforge（conda）、git、adb
brew install miniforge git android-platform-tools
```

**第二步：下載專案並建立環境**

```bash
git clone https://github.com/jhihlinglu/AzurLaneAutoScript.git
cd AzurLaneAutoScript

# 建立 Python 環境（需幾分鐘）
CONDA_CHANNEL_PRIORITY=flexible conda env create -f environment-arm-mac.yml

# 修復 macOS 動態函式庫問題
conda activate alas
bash deploy/mac/fix_rpath.sh
```

**第三步：設定 deploy.yaml**

```bash
cp config/deploy.template-mac.yaml config/deploy.yaml
```

用文字編輯器開啟 `config/deploy.yaml`，找到這行：

```
PythonExecutable: /Users/username/miniforge3/envs/alas/bin/python
```

把 `username` 換成你的 Mac 使用者名稱（或執行 `conda activate alas && which python` 取得正確路徑）。

**第四步：連接模擬器**

1. 下載並安裝 [BlueStacks for Mac](https://www.bluestacks.com/mac)
2. 開啟 BlueStacks → 右上角「齒輪」→ 偏好設定 → 進階 → 開啟 **Android Debug Bridge（ADB）**
3. 設定解析度：顯示 → `1280 × 720`，選「平板」模式
4. 回到終端機執行：

```bash
adb connect 127.0.0.1:5555
```

**第五步：啟動 Alas**

```bash
conda activate alas
cd AzurLaneAutoScript
python gui.py
```

開啟瀏覽器，前往 **http://127.0.0.1:22267**

在 Alas 設定頁面，將 `Alas → Emulator → Serial` 設為 `127.0.0.1:5555`，即可開始使用。

### 常見問題

| 問題 | 解決方式 |
|---|---|
| `ImportError: libgfortran` | 執行 `bash deploy/mac/fix_rpath.sh` |
| conda env create 失敗 | 確認指令前有加 `CONDA_CHANNEL_PRIORITY=flexible` |
| ADB 連不上模擬器 | 確認 BlueStacks 有開啟 ADB，並重新執行 `adb connect 127.0.0.1:5555` |

---

## English

Alas is an Azur Lane automation bot with a web GUI, supporting CN / EN / JP / TW servers. Designed for 24/7 operation — it can handle almost all in-game content automatically.

Original project: [LmeSzinc/AzurLaneAutoScript](https://github.com/LmeSzinc/AzurLaneAutoScript)
This fork adds native **Apple Silicon (ARM) Mac** support.

### Features

- Sorties: story maps, event maps, co-op, emergency commissions
- Collection: commissions, academy, research, dorm, daily gacha
- Daily: daily quests, hard maps, exercise, submarine maps
- META: monthly meta, hidden zones, abyss, siren stronghold

### Installation (Apple Silicon Mac)

> Requires M1 / M2 / M3 / M4, macOS 12 or later

**Step 1 — Install prerequisites**

Open **Terminal** and run these commands one by one:

```bash
# Install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install miniforge (conda), git, adb
brew install miniforge git android-platform-tools
```

**Step 2 — Download and set up the environment**

```bash
git clone https://github.com/jhihlinglu/AzurLaneAutoScript.git
cd AzurLaneAutoScript

# Create Python environment (takes a few minutes)
CONDA_CHANNEL_PRIORITY=flexible conda env create -f environment-arm-mac.yml

# Fix macOS dynamic library issues
conda activate alas
bash deploy/mac/fix_rpath.sh
```

**Step 3 — Configure deploy.yaml**

```bash
cp config/deploy.template-mac.yaml config/deploy.yaml
```

Open `config/deploy.yaml` in a text editor and update this line:

```
PythonExecutable: /Users/username/miniforge3/envs/alas/bin/python
```

Replace `username` with your Mac username. (Or run `conda activate alas && which python` to get the exact path.)

**Step 4 — Connect an emulator**

1. Download and install [BlueStacks for Mac](https://www.bluestacks.com/mac)
2. Open BlueStacks → top-right gear icon → Preferences → Advanced → enable **Android Debug Bridge (ADB)**
3. Set resolution: Display → `1280 × 720`, select **Tablet** mode
4. Back in Terminal, run:

```bash
adb connect 127.0.0.1:5555
```

**Step 5 — Launch Alas**

```bash
conda activate alas
cd AzurLaneAutoScript
python gui.py
```

Open your browser and go to **http://127.0.0.1:22267**

In the Alas settings page, set `Alas → Emulator → Serial` to `127.0.0.1:5555`.

### Troubleshooting

| Problem | Fix |
|---|---|
| `ImportError: libgfortran` | Run `bash deploy/mac/fix_rpath.sh` |
| `conda env create` fails | Make sure to prefix the command with `CONDA_CHANNEL_PRIORITY=flexible` |
| ADB can't connect | Confirm ADB is enabled in BlueStacks, then re-run `adb connect 127.0.0.1:5555` |

---

## 日本語

Alas は Web GUI 付きの碧ブレイン自動化スクリプトです。CN / EN / JP / TW サーバーに対応し、24 時間稼働を前提に設計されています。ほぼすべてのゲームコンテンツを自動化できます。

オリジナルプロジェクト：[LmeSzinc/AzurLaneAutoScript](https://github.com/LmeSzinc/AzurLaneAutoScript)
この Fork では **Apple Silicon（ARM）Mac** のネイティブ動作を追加サポートしています。

### 主な機能

- 出撃：ストーリー海域、イベント海域、共闘、緊急委託
- 収穫：委託、戦術教室、科研、寮、デイリーガチャ
- デイリー：デイリー任務、ハード海域、演習、潜水艦海域
- 大世界：月次開拓、潜伏海域、深淵海域、セイレーン要塞

### インストール手順（Apple Silicon Mac）

> M1 / M2 / M3 / M4、macOS 12 以降が必要です

**ステップ 1 — 必要ツールのインストール**

「ターミナル」を開き、以下のコマンドを一行ずつ実行します：

```bash
# Homebrew のインストール
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# miniforge（conda）、git、adb のインストール
brew install miniforge git android-platform-tools
```

**ステップ 2 — プロジェクトのダウンロードと環境構築**

```bash
git clone https://github.com/jhihlinglu/AzurLaneAutoScript.git
cd AzurLaneAutoScript

# Python 環境の作成（数分かかります）
CONDA_CHANNEL_PRIORITY=flexible conda env create -f environment-arm-mac.yml

# macOS のダイナミックライブラリ問題を修正
conda activate alas
bash deploy/mac/fix_rpath.sh
```

**ステップ 3 — deploy.yaml の設定**

```bash
cp config/deploy.template-mac.yaml config/deploy.yaml
```

テキストエディタで `config/deploy.yaml` を開き、以下の行を編集します：

```
PythonExecutable: /Users/username/miniforge3/envs/alas/bin/python
```

`username` を自分の Mac ユーザー名に変更してください。（`conda activate alas && which python` で正確なパスを確認できます。）

**ステップ 4 — エミュレーターの接続**

1. [BlueStacks for Mac](https://www.bluestacks.com/mac) をダウンロード・インストール
2. BlueStacks を起動 → 右上の歯車アイコン → 設定 → 詳細設定 → **Android Debug Bridge（ADB）** を有効化
3. 解像度を設定：ディスプレイ → `1280 × 720`、**タブレット**モードを選択
4. ターミナルで以下を実行：

```bash
adb connect 127.0.0.1:5555
```

**ステップ 5 — Alas の起動**

```bash
conda activate alas
cd AzurLaneAutoScript
python gui.py
```

ブラウザで **http://127.0.0.1:22267** を開きます。

Alas の設定画面で `Alas → Emulator → Serial` を `127.0.0.1:5555` に設定すれば完了です。

### トラブルシューティング

| 問題 | 解決方法 |
|---|---|
| `ImportError: libgfortran` | `bash deploy/mac/fix_rpath.sh` を実行 |
| `conda env create` が失敗する | コマンドの前に `CONDA_CHANNEL_PRIORITY=flexible` を付けているか確認 |
| ADB が接続できない | BlueStacks で ADB が有効になっているか確認し、`adb connect 127.0.0.1:5555` を再実行 |

---

## 한국어

Alas는 웹 GUI를 갖춘 벽람항로 자동화 봇입니다. CN / EN / JP / TW 서버를 지원하며, 24시간 연속 실행을 목표로 설계되었습니다. 게임 내 거의 모든 콘텐츠를 자동으로 처리합니다.

원본 프로젝트：[LmeSzinc/AzurLaneAutoScript](https://github.com/LmeSzinc/AzurLaneAutoScript)
이 Fork는 **Apple Silicon（ARM）Mac** 네이티브 지원을 추가했습니다.

### 주요 기능

- 출격：스토리 해역, 이벤트 해역, 공동작전, 긴급임무
- 수확：임무, 전술학원, 연구, 기숙사, 일일 가챠
- 일일：일일 임무, 하드 해역, 연습, 잠수함 해역
- 대세계：월간 개척, 은밀 해역, 심연 해역, 사이렌 요새

### 설치 방법（Apple Silicon Mac）

> M1 / M2 / M3 / M4, macOS 12 이상 필요

**1단계 — 필수 도구 설치**

「터미널」을 열고 아래 명령어를 한 줄씩 실행합니다：

```bash
# Homebrew 설치
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# miniforge（conda）, git, adb 설치
brew install miniforge git android-platform-tools
```

**2단계 — 프로젝트 다운로드 및 환경 구성**

```bash
git clone https://github.com/jhihlinglu/AzurLaneAutoScript.git
cd AzurLaneAutoScript

# Python 환경 생성（몇 분 소요）
CONDA_CHANNEL_PRIORITY=flexible conda env create -f environment-arm-mac.yml

# macOS 동적 라이브러리 문제 수정
conda activate alas
bash deploy/mac/fix_rpath.sh
```

**3단계 — deploy.yaml 설정**

```bash
cp config/deploy.template-mac.yaml config/deploy.yaml
```

텍스트 편집기로 `config/deploy.yaml` 을 열고 아래 줄을 수정합니다：

```
PythonExecutable: /Users/username/miniforge3/envs/alas/bin/python
```

`username` 을 본인의 Mac 사용자 이름으로 변경하세요. （`conda activate alas && which python` 으로 정확한 경로 확인 가능）

**4단계 — 에뮬레이터 연결**

1. [BlueStacks for Mac](https://www.bluestacks.com/mac) 다운로드 및 설치
2. BlueStacks 실행 → 오른쪽 상단 톱니바퀴 → 환경설정 → 고급 → **Android Debug Bridge（ADB）** 활성화
3. 해상도 설정：디스플레이 → `1280 × 720`, **태블릿** 모드 선택
4. 터미널에서 실행：

```bash
adb connect 127.0.0.1:5555
```

**5단계 — Alas 실행**

```bash
conda activate alas
cd AzurLaneAutoScript
python gui.py
```

브라우저에서 **http://127.0.0.1:22267** 접속

Alas 설정 화면에서 `Alas → Emulator → Serial` 을 `127.0.0.1:5555` 로 설정하면 완료입니다.

### 문제 해결

| 문제 | 해결 방법 |
|---|---|
| `ImportError: libgfortran` | `bash deploy/mac/fix_rpath.sh` 실행 |
| `conda env create` 실패 | 명령어 앞에 `CONDA_CHANNEL_PRIORITY=flexible` 가 있는지 확인 |
| ADB 연결 불가 | BlueStacks에서 ADB가 활성화되어 있는지 확인 후 `adb connect 127.0.0.1:5555` 재실행 |

---

*Fork maintained by [@jhihlinglu](https://github.com/jhihlinglu) · Original project by [@LmeSzinc](https://github.com/LmeSzinc)*
