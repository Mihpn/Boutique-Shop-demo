# Stage 1: Build (Nhà xưởng)
# Dùng Alpine 3.19 cho ổn định (tránh dùng bản 3.14.2 quá cũ và có mã SHA cứng)
FROM python:3.12-alpine AS builder

WORKDIR /app

# Thiết lập biến môi trường để Python chạy mượt hơn
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Cài đặt đồ nghề để compile các thư viện C++ (như grpcio)
RUN apk add --no-cache g++ linux-headers libstdc++

# 🚨 BÍ KÍP TỐI ƯU: Tạo môi trường ảo (venv)
RUN python -m venv /opt/venv
# Đảm bảo pip dùng trong venv
ENV PATH="/opt/venv/bin:$PATH"

# Tận dụng Docker Cache cho requirements
COPY requirements.txt .

# Cài đặt thư viện VÀO TRONG MÔI TRƯỜNG ẢO
RUN pip install --no-cache-dir -r requirements.txt


# Stage 2: Runtime (Thành phẩm siêu nhẹ)
FROM python:3.12-alpine

LABEL maintainer="kihpn1711"
LABEL service="emailservice"

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Cài thêm libstdc++ vì grpcio cần nó để chạy lúc runtime
RUN apk add --no-cache libstdc++

# 🚨 CHỈ rinh đúng cái môi trường ảo đã cài xong thư viện từ nhà xưởng sang
COPY --from=builder /opt/venv /opt/venv

# Thiết lập PATH để Python tự hiểu là phải dùng thư viện trong venv
ENV PATH="/opt/venv/bin:$PATH"

# Rinh nốt source code của app vào
COPY . .

# EmailService không mở cổng (Nó là worker lắng nghe RabbitMQ/PubSub hoặc gRPC)
# Nên ta không cần lệnh EXPOSE ở đây.
# Khởi chạy ứng dụng
ENTRYPOINT ["python", "email_server.py"]
