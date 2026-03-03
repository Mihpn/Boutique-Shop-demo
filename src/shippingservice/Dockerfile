# Stage 1: Build (Nhà xưởng)
FROM golang:1.22-alpine AS builder

WORKDIR /app

# Khôi phục thư viện trước để tận dụng Docker Cache
COPY go.mod go.sum ./
RUN go mod download

# Copy code vào và đóng gói
COPY . .

# Lệnh build ép cân (xóa debug info) giúp file binary cực nhẹ
RUN CGO_ENABLED=0 go build -ldflags="-s -w" -o /app/shippingservice .

# Stage 2: Runtime (Thành phẩm)
FROM alpine:3.19

WORKDIR /app

# Rinh đúng cái file chạy từ nhà xưởng sang
COPY --from=builder /app/shippingservice /app/shippingservice

# Các biến môi trường cần thiết của ShippingService
ENV APP_PORT=50051
ENV GOTRACEBACK=single

# Mở cổng giao tiếp
EXPOSE 50051

# Khởi chạy ứng dụng
ENTRYPOINT ["/app/shippingservice"]
