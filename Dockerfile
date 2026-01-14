# ベースイメージとしてPythonの公式イメージを使用
FROM python:3.13-slim

# Gitをインストール
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir --upgrade pip setuptools wheel

# 作業ディレクトリを/appに設定
WORKDIR /app

# requirements.txtをコンテナにコピー
COPY ./requirements.txt .
# 依存関係をインストール
RUN pip install -r requirements.txt

# スクリプトをコンテナにコピー
COPY ./psd_maskdata ./psd_maskdata
COPY ./settings.yaml .
COPY ./pyproject.toml .

# 標準出力がバッファリングされないよう設定（C#側でリアルタイムに進捗を拾うため）
ENV PYTHONUNBUFFERED=1

# コンテナ起動時のデフォルトコマンド
ENTRYPOINT ["python", "-m", "psd_maskdata"]
CMD []

# メタデータの追加
LABEL org.opencontainers.image.source="https://github.com/bteam-toku/psd_maskdata_develop.git"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.description="PSDマスク情報エクスポート（Dockerコンテナ）"