# Stage 1: Build (Nhà xưởng Go)
FROM golang:1.25-alpine AS builder

WORKDIR /app

# Tận dụng cache của Docker: Tải thư viện trước
COPY go.mod go.sum ./
RUN go mod download

# Copy toàn bộ code (Bao gồm cả file products.json)
COPY . .

# Ép cân và build ra cục binary tên là 'server'
RUN CGO_ENABLED=0 go build -ldflags="-s -w" -o /app/server .


# Stage 2: Runtime (Thành phẩm siêu nhẹ, có Shell)
FROM alpine:3.19

WORKDIR /app

# 1. Rinh file chạy từ nhà xưởng sang
COPY --from=builder /app/server .

# 2. 🚨 QUAN TRỌNG: Rinh theo file data sản phẩm
COPY products.json .

# Các biến môi trường
ENV GOTRACEBACK=single
EXPOSE 3550

# Khởi chạy
ENTRYPOINT ["/app/server"]
