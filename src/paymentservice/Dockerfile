# Stage 1: Build
FROM node:20-alpine AS builder

WORKDIR /app

RUN apk add --no-cache python3 make g++
COPY package*.json ./

RUN npm install --only=production

# Stage 2: Runtime
FROM node:20-alpine
ENV DISABLE_PROFILER=1
WORKDIR /app


COPY --from=builder /app/node_modules ./node_modules
COPY . .

EXPOSE 50051
ENTRYPOINT [ "node", "index.js" ]
