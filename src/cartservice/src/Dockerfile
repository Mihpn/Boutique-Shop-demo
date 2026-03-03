
FROM mcr.microsoft.com/dotnet/sdk:10.0-noble AS builder

WORKDIR /src

COPY cartservice.csproj .
RUN dotnet restore cartservice.csproj
COPY . .

# Build
RUN dotnet publish cartservice.csproj \
    -p:PublishSingleFile=true \
    --self-contained true \
    -p:PublishTrimmed=true \
    -p:TrimMode=full \
    -c release \
    -o /app/published

# Stage 2: Runtime

FROM mcr.microsoft.com/dotnet/runtime-deps:10.0-noble

WORKDIR /app

COPY --from=builder /app/published .
EXPOSE 7070
ENV ASPNETCORE_HTTP_PORTS=7070
ENV DOTNET_EnableDiagnostics=0


ENTRYPOINT ["/app/cartservice"]
