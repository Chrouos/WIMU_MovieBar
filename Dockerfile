# 使用官方 Python 基礎映像
FROM python:3.9-slim

# 設定工作目錄
WORKDIR /app

# 複製本地代碼和 requirements.txt 到容器中
COPY . /app
COPY requirements.txt /app/

# 安裝依賴
RUN pip install --no-cache-dir -r requirements.txt

# 開放端口 8150 供外部訪問
EXPOSE 8150

# 啟動 Flask 應用
CMD ["flask", "run", "--host=0.0.0.0", "--port=8150"]

# docker build -t flask-chat-app .
# docker run -d -p 8150:8150 --name flask_chat_app -v ${PWD}/data:/app/data flask-chat-app