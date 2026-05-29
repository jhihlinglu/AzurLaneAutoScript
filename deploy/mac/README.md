# Apple Silicon (ARM) Mac 安裝說明

適用於 M1/M2/M3/M4 系列 Mac，macOS 12+。

## 前置需求

```bash
brew install miniforge git android-platform-tools
```

## 安裝步驟

### 1. 建立 conda 環境

```bash
git clone https://github.com/LmeSzinc/AzurLaneAutoScript.git
cd AzurLaneAutoScript
CONDA_CHANNEL_PRIORITY=flexible conda env create -f environment-arm-mac.yml
```

> **為什麼需要 `CONDA_CHANNEL_PRIORITY=flexible`？**
> `environment-arm-mac.yml` 同時使用 `anaconda` 和 `conda-forge` 兩個 channel，
> 因為 mxnet 1.5.1 的 ARM64 原生版本只存在於 `anaconda` channel。

### 2. 修復動態函式庫 rpath 問題

macOS 12+ 的動態連結器對重複 rpath 更嚴格，會導致 numpy/mxnet 無法 import。
執行以下腳本修復：

```bash
conda activate alas
bash deploy/mac/fix_rpath.sh
```

### 3. 建立 deploy.yaml

```bash
cp config/deploy.template-mac.yaml config/deploy.yaml
```

編輯 `config/deploy.yaml`，將 `PythonExecutable` 改為你的實際路徑：

```bash
which python  # 在 conda activate alas 後執行
```

### 4. 啟動 ALAS

```bash
conda activate alas
python gui.py
```

開啟瀏覽器訪問：http://127.0.0.1:22267

## 連接模擬器

### BlueStacks for Mac（推薦）

1. 下載 [BlueStacks for Mac](https://www.bluestacks.com/mac)
2. 設定解析度為 `1280×720`、平板模式
3. 進階設定 → 開啟 ADB 除錯
4. 連接 ADB：

```bash
adb connect 127.0.0.1:5555
```

5. 在 ALAS 設定中將 `Alas.Emulator.Serial` 設為 `127.0.0.1:5555`

### 實體 Android 裝置

透過 USB 連接後，直接在 ALAS 設定中選擇裝置序號即可。

## 常見問題

**Q: `ImportError: Library not loaded: @rpath/libgfortran.5.dylib`**
A: 執行 `bash deploy/mac/fix_rpath.sh` 修復。

**Q: `conda env create` 失敗，出現 `excluded by strict repo priority`**
A: 確認指令前有加 `CONDA_CHANNEL_PRIORITY=flexible`。

**Q: `which python` 回傳 `not found`**
A: 確認已執行 `conda activate alas`，或建立軟連結：
```bash
ln -s $(conda run -n alas which python) /usr/local/bin/python
```
