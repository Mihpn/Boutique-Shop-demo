# Stage 1: Build (Sử dụng Alpine nhưng cài thêm glibc compatibility)
FROM eclipse-temurin:21-jdk-alpine AS builder

WORKDIR /app

# 🚨 CÀI THÊM gcompat để chạy được protoc binary trên Alpine
RUN apk add --no-cache gcompat

COPY build.gradle gradlew ./
COPY gradle gradle

# Cấp quyền và chạy (Lúc này protoc-gen-grpc sẽ chạy được)
RUN chmod +x gradlew && ./gradlew downloadRepos

COPY . .
RUN chmod +x gradlew
RUN ./gradlew installDist

# Stage 2: Giữ nguyên như cũ (vì Stage 2 chỉ chạy file .jar/.class, không cần protoc nữa)
FROM eclipse-temurin:21-jre-alpine
WORKDIR /app
COPY --from=builder /app/build/install/hipstershop /app/
EXPOSE 9555
ENTRYPOINT ["/app/bin/AdService"]
