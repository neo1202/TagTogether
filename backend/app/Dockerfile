FROM python:3.9

RUN apt-get update
RUN pip install --upgrade pip


# WORKDIR /app：設置容器內的工作目錄為 /app。
# COPY . .：將 build context 中的所有文件複製到 /app 中。
WORKDIR /app
# 複製依賴文件並安裝
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 複製程式碼
# 將 build context 中的所有文件複製到 /app 中。
COPY . /app/   

# 開放端口
EXPOSE 8000

# 預設命令（Docker Compose 中會覆蓋這裡）
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
