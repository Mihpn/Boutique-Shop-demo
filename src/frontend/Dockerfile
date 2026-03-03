# Stage 1: Build the application
# Sử dụng Alpine để có môi trường build nhẹ nhưng đầy đủ công cụ Go
FROM golang:1.25-alpine AS builder

WORKDIR /app

# Copy các file quản lý thư viện trước để tối ưu hóa cache
COPY go.mod go.sum ./
RUN go mod download

# Copy toàn bộ mã nguồn vào để build
COPY . .

# Build file thực thi (Binary)
# -ldflags="-s -w" giúp xóa bỏ debug info, làm file cực nhẹ
RUN CGO_ENABLED=0 go build -ldflags="-s -w" -o /app/frontend-binary .

# Stage 2: Run the application
# Sử dụng Alpine làm môi trường chạy để bạn có thể vào shell debug khi cần
FROM alpine:3.19

WORKDIR /app

# Chỉ copy file thực thi duy nhất từ Stage 1 sang
COPY --from=builder /app/frontend-binary /app/server

# Với Go Frontend, ta cần copy thêm các thư mục giao diện tĩnh
COPY ./templates ./templates
COPY ./static ./static

# Khai báo port ứng dụng chạy
EXPOSE 8080

# Chạy ứng dụng
ENTRYPOINT ["/app/server"]
