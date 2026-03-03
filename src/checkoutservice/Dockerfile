# Stage 1: Build the application
# Dùng Alpine làm nhà xưởng để có đầy đủ đồ nghề build Go
FROM golang:1.22-alpine AS builder

WORKDIR /app

# Khôi phục thư viện (Tận dụng sức mạnh Docker Cache như đã nói ở trên)
COPY go.mod go.sum ./
RUN go mod download

# Copy toàn bộ code vào để chuẩn bị xào nấu
COPY . .

# Build ra file thực thi (Binary)
# Vẫn giữ nguyên bùa chú -ldflags="-s -w" để ép cân file binary
RUN CGO_ENABLED=0 go build -ldflags="-s -w" -o /app/checkoutservice .

# Stage 2: Run the application
# Dùng Alpine siêu nhẹ làm môi trường chạy, cho phép bạn chui vào shell (sh) khi cần gỡ lỗi
FROM alpine:3.19

# Thêm nhãn mác cho chuyên nghiệp
LABEL maintainer="your-dockerhub-username"
LABEL service="checkoutservice"

WORKDIR /app

# Chỉ rinh đúng cái file đã build xong từ nhà xưởng sang
COPY --from=builder /app/checkoutservice /app/checkoutservice

# Biến môi trường hệ thống của Go
ENV GOTRACEBACK=single

# Con checkout này mở cổng 5050 để các service khác gọi tới
EXPOSE 5050

# Khởi chạy "nhạc trưởng"
ENTRYPOINT ["/app/checkoutservice"]
