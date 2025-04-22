# 使用官方 Python 基底映像
FROM python:3.9-slim

# 設定工作目錄
WORKDIR /app

# 複製專案檔案到容器中
COPY . .

# 安裝 Python 套件
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 對外開放 8000 port
EXPOSE 8000

# 啟動 Django 開發伺服器
CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
