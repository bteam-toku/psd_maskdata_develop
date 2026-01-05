# ベースイメージとしてPythonの公式イメージを使用
FROM python:3.13-slim

# Gitをインストール
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# 作業ディレクトリを/appに設定
WORKDIR /app

# requirements.txtをコンテナにコピー
COPY requirements.txt .

# 依存関係をインストール
RUN pip install --no-cache-dir -r requirements.txt

# スクリプトをコンテナにコピー
COPY ./psd_maskdata ./psd_maskdata

# コンテナ起動時のデフォルトコマンド
ENTRYPOINT ["python", "-m", "psd_maskdata"]
