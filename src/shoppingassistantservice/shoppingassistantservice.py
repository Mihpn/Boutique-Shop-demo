#!/usr/bin/python
# shoppingassistantservice.py — Gemini REST API (zero SDK)
# Auto-tries v1beta → v1 fallback to handle API key differences.
# Interface: POST / → {"content":"..."} | GET /health → {"status":"ok"}

import os, sys, base64, json, logging, urllib.request, urllib.error
from flask import Flask, request, jsonify

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("shoppingassistant")

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
GEMINI_MODEL   = os.environ.get("GEMINI_MODEL", "gemini-1.5-flash").strip()
GEMINI_TIMEOUT = int(os.environ.get("GEMINI_TIMEOUT", "30"))
PORT           = int(os.environ.get("PORT", "8080"))

GEMINI_BASE    = "https://generativelanguage.googleapis.com"

# Try these API versions in order — newer keys may only work with v1
API_VERSIONS   = ["v1beta", "v1"]

SYSTEM_PROMPT = (
    "You are a helpful shopping assistant for Online Boutique e-commerce store. "
    "Suggest relevant products based on the customer's request. Be concise and friendly."
)

if GEMINI_API_KEY:
    logger.info("Ready | model=%s key=...%s", GEMINI_MODEL, GEMINI_API_KEY[-4:])
else:
    logger.warning("GEMINI_API_KEY not set — will return fallback responses.")


# ---------------------------------------------------------------------------
# Gemini REST call with version fallback
# ---------------------------------------------------------------------------
def call_gemini(user_text: str, image_data: str = "") -> str:
    """
    Tries API versions in order (v1beta → v1) until one succeeds.
    This handles both legacy and new Gemini API keys.
    """
    # Read env vars fresh per-request (avoids stale module-level state)
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    model   = os.environ.get("GEMINI_MODEL", GEMINI_MODEL).strip()

    parts = [{"text": SYSTEM_PROMPT + "\n\n" + user_text}]

    if image_data:
        img = _parse_image(image_data)
        if img:
            parts.insert(0, img)

    payload = json.dumps({
        "contents": [{"role": "user", "parts": parts}],
        "generationConfig": {"maxOutputTokens": 512, "temperature": 0.7},
    }).encode("utf-8")

    last_err = None
    for version in API_VERSIONS:
        url = f"{GEMINI_BASE}/{version}/models/{model}:generateContent?key={api_key}"
        logger.info("Trying %s/%s", version, model)
        try:
            req = urllib.request.Request(
                url, data=payload,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=GEMINI_TIMEOUT) as resp:
                result = json.loads(resp.read().decode("utf-8"))
            candidates = result.get("candidates", [])
            if not candidates:
                raise ValueError(f"No candidates returned: {result}")
            text = " ".join(
                p.get("text", "")
                for p in candidates[0].get("content", {}).get("parts", [])
            ).strip()
            logger.info("OK via %s | reply_len=%d", version, len(text))
            return text

        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            logger.warning("HTTP %d from %s: %s", e.code, version, body[:300])
            if e.code == 404:
                last_err = e
                continue          # try next version
            raise                 # other errors (401, 429…) → stop immediately
        except Exception as e:
            last_err = e
            logger.warning("Error with %s: %s", version, e)
            continue

    raise last_err or RuntimeError("All API versions failed")


def _parse_image(image_data: str) -> dict | None:
    try:
        if image_data.startswith("data:"):
            header, b64 = image_data.split(",", 1)
            mime = header.split(";")[0].replace("data:", "") or "image/jpeg"
            return {"inline_data": {"mime_type": mime, "data": b64}}
        if image_data.startswith(("http://", "https://")):
            req = urllib.request.Request(image_data,
                                         headers={"User-Agent": "ShoppingAssistant/2.0"})
            with urllib.request.urlopen(req, timeout=10) as r:
                b64  = base64.b64encode(r.read()).decode()
                mime = r.headers.get_content_type() or "image/jpeg"
            return {"inline_data": {"mime_type": mime, "data": b64}}
    except Exception as e:
        logger.warning("Image skipped: %s", e)
    return None


# ---------------------------------------------------------------------------
# Flask app
# ---------------------------------------------------------------------------
def create_app() -> Flask:
    app = Flask(__name__)

    @app.route("/health", methods=["GET"])
    @app.route("/healthz", methods=["GET"])
    def health():
        return jsonify({"status": "ok"}), 200

    @app.route("/test-api", methods=["GET"])
    def test_api():
        """Debug: lists models available for your API key."""
        api_key = os.environ.get("GEMINI_API_KEY", "").strip()
        if not api_key:
            return jsonify({"error": "GEMINI_API_KEY not set"}), 400
        results = {}
        for ver in API_VERSIONS:
            url = f"{GEMINI_BASE}/{ver}/models?key={api_key}"
            try:
                with urllib.request.urlopen(url, timeout=10) as r:
                    data = json.loads(r.read())
                    models = [m["name"] for m in data.get("models", [])]
                    results[ver] = {"count": len(models), "models": models[:10]}
            except urllib.error.HTTPError as e:
                results[ver] = {"error": e.code, "body": e.read().decode()[:200]}
            except Exception as e:
                results[ver] = {"error": str(e)}
        return jsonify(results), 200

    @app.route("/", methods=["POST"])
    def chat():
        if not os.environ.get("GEMINI_API_KEY", "").strip():
            return jsonify({"content": (
                "Shopping Assistant offline (no API key). "
                "Browse our catalog — great products await!"
            )}), 200

        body    = request.get_json(force=True, silent=True) or {}
        message = (body.get("message") or "").strip()
        image   = (body.get("image")   or "").strip()

        if not message:
            return jsonify({"content": "What are you looking for today?"}), 200

        logger.info("Request | msg_len=%d has_image=%s", len(message), bool(image))
        try:
            reply = call_gemini(message, image)
            return jsonify({"content": reply}), 200
        except urllib.error.HTTPError as e:
            body_text = e.read().decode("utf-8", errors="replace")
            logger.error("Final HTTP error %d: %s", e.code, body_text[:500])
            hint = ""
            if e.code == 401:
                hint = " (API key invalid or expired)"
            elif e.code == 429:
                hint = " (rate limit — try again later)"
            return jsonify({"content": f"AI model error {e.code}{hint}. Try again!"}), 200
        except Exception as exc:
            logger.error("Error: %s", exc, exc_info=True)
            return jsonify({"content": "Something went wrong. Please try again!"}), 200

    return app


if __name__ == "__main__":
    app = create_app()
    logger.info("Starting on :%d | model=%s", PORT, GEMINI_MODEL)
    app.run(host="0.0.0.0", port=PORT, debug=False, threaded=True)
