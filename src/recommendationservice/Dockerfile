# Stage 1: Build (Nhà xưởng)
FROM python:3.12-alpine AS builder

WORKDIR /app

# Thiết lập môi trường Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Cài đồ nghề compile C++ cho thằng grpcio
RUN apk add --no-cache g++ linux-headers libstdc++

# 🚨 DÙNG BÀI TỦ: Tạo môi trường ảo (venv)
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy file requirements và cài đặt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime (Thành phẩm siêu nhẹ)
FROM python:3.12-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Cài thư viện C++ runtime cho grpcio
RUN apk add --no-cache libstdc++

# Rinh môi trường ảo đã đóng gói sẵn sang
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Rinh code ứng dụng sang
COPY . .

# Đặt cổng nội bộ (Không sợ đụng hàng với Frontend)
ENV PORT="8080"
EXPOSE 8080

# Chạy ứng dụng
ENTRYPOINT ["python", "recommendation_server.py"]
