# Node.js 20の軽量イメージを使用
FROM node:20-alpine

# 作業ディレクトリを設定
WORKDIR /app

# package.jsonとpackage-lock.jsonをコピー
COPY package*.json ./

# 依存関係をインストール
RUN npm install

# アプリケーションコードをコピー（ボリュームマウントするが、初期ビルド用）
COPY . .

# ポート3000を公開
EXPOSE 3000

# 開発サーバーを起動（ホットリロード有効）
CMD ["npm", "run", "dev"]
