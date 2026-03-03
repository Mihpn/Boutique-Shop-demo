# Stage 1: Build (Nhà xưởng)
FROM node:20-alpine AS builder

WORKDIR /app

# Vẫn phải cài đồ nghề C++ cho mấy thư viện của Google
RUN apk add --no-cache python3 make g++

COPY package*.json ./

# Dùng lệnh này cho an toàn, đỡ bị văng lỗi lockfile khi làm Lab
RUN npm install --only=production

# Stage 2: Runtime (Thành phẩm)
FROM node:20-alpine
ENV DISABLE_PROFILER=1
WORKDIR /app

# Rinh node_modules đã compile chuẩn xác từ nhà xưởng sang
COPY --from=builder /app/node_modules ./node_modules

# Rinh code ứng dụng vào
COPY . .

# Mở cổng 7000 (Thay vì 50051 như Payment)
EXPOSE 7000

# File khởi động của con này là server.js
ENTRYPOINT [ "node", "server.js" ]
