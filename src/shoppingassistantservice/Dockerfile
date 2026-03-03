# Stage 1: Build
FROM python:3.12-slim AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Only Flask — no C extensions needed at all
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ──────────────────────────────────────────────
# Stage 2: Runtime — super lean (~120MB total)
FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080 \
    GEMINI_MODEL=gemini-1.5-flash \
    GEMINI_TIMEOUT=30

COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY shoppingassistantservice.py .

EXPOSE 8080

# Non-root — matches K8s runAsUser: 1000
RUN useradd -u 1000 -m appuser
USER appuser

ENTRYPOINT ["python", "shoppingassistantservice.py"]
