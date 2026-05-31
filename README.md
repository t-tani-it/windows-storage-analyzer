# windows-storage-analyzer
# フォルダ容量スキャナー（Windows）

Windows の指定フォルダ以下を走査し、2 階層までのフォルダ容量を調べて表示する Python スクリプトです。指定した閾値以上のフォルダだけを一覧表示します。

---

## 機能
- 指定したフォルダ直下のサブフォルダを走査
- 2 階層目までのフォルダ容量を取得
- 指定したサイズ（MB）以上のフォルダのみを表示
- Windows エクスプローラーと同じ「物理ディスク使用量」を取得

---

## 対応環境
- Python 3
- Windows API（GetCompressedFileSizeW）を使用するため、Linux / macOS では動作しません

---

## 使い方

### 1. クローン
```bash
git clone https://github.com/t-tani-it/windows-storage-analyzer.git
cd windows-storage-analyzer
```

### 2. インストール
このプロジェクトは Python 標準ライブラリのみで動作します。
必要な外部パッケージはありません。

### 3. 設定
`src/main.py` の先頭にある以下の部分で、デフォルト値を変更できます。

```python
DEFAULT_TARGET_DIR = r"C:\Users"
DEFAULT_THRESHOLD_MB = 100
```

- `DEFAULT_TARGET_DIR` : デフォルトで調べるフォルダのパス
- `DEFAULT_THRESHOLD_MB` : デフォルトで表示する最小サイズ（MB）

### 4. 実行
```bash
python src/main.py
```

#### 4.1 コマンドライン引数で指定する場合
```bash
python src/main.py C:\path\to\folder 100
```

- 1 個目の引数: 調べたいフォルダ
- 2 個目の引数: 表示する最小サイズ（MB）

### 5. 例
`python src/main.py C:\Users 100` を実行すると、100 MB 以上のフォルダが表示されます。

---

## 追加メモ
- `requirements.txt` は現在、外部ライブラリを使っていないため空です。
- コマンドライン引数に対応しています。

### 工夫した点
- 当初は、100MB以下の比較的小さいファイルも列挙されていたが、閾値フィルタを設けました
- また、使いやすさ向上のため、CLIにて引数を指定できるように改良しました

### 今後の改善点
- 現在、2階層を対象としているが、検索対象の深さもユーザーにて指定できるように改善する
