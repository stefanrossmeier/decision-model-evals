#!/usr/bin/env python3
"""Thin System One HTTP transport around Julia 1's native named-question API."""
from __future__ import annotations

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import argparse
import json
import sys
import time

MODEL = "SupersonicLabs/Julia-1"
REVISION = "a85b127321d580d65176c89ced8273f305745d85"
WEIGHTS_SHA256 = "df853bf7fe424420011f3d0c47a05d7341aa9eefa7fb9f203ea4aada4ad95b72"


def build_runtime(checkpoint: str, device: str):
    from julia import load_model

    return load_model(
        checkpoint,
        device=device,
        strict_encoding=True,
        max_length=8192,
        head_length=512,
        marker_only_head=False,
    )


def predict_payload(engine, payload):
    if not isinstance(payload, dict):
        raise ValueError("request body must be a JSON object")
    questions = payload.get("questions")
    if not isinstance(questions, dict) or not questions:
        raise ValueError("questions must be a nonempty mapping")
    result = engine.predict(state=payload.get("state"), questions=questions)
    if not isinstance(result, dict) or not isinstance(result.get("answers"), dict):
        raise ValueError("Julia returned an invalid named-question response")
    return result


def configure_handler(engine, metadata):
    Handler.engine = engine
    Handler.metadata = metadata


class Handler(BaseHTTPRequestHandler):
    engine = None
    metadata = None

    def log_message(self, fmt, *args):
        return

    def _send(self, status, body):
        data = json.dumps(body, allow_nan=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path == "/health":
            self._send(200, {"status": "ok", "model": MODEL, "revision": REVISION, **self.metadata})
        else:
            self._send(404, {"error": "not found"})

    def do_POST(self):
        if self.path != "/v1/systemone":
            return self._send(404, {"error": "not found"})
        try:
            n = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(n))
            started = time.perf_counter()
            result = predict_payload(self.engine, payload)
            elapsed_ms = (time.perf_counter() - started) * 1000.0
            self._send(
                200,
                {
                    "model": f"{MODEL}@{REVISION}",
                    "provider": "julia1",
                    "answers": result["answers"],
                    "elapsed_ms": elapsed_ms,
                    "runtime": self.metadata,
                    "usage": {"output_tokens": 0},
                },
            )
        except Exception as exc:  # noqa: BLE001 - server must report inference failures
            message = f"{type(exc).__name__}: {exc}"
            print(f"Julia 1 request failed: {message}", file=sys.stderr, flush=True)
            self._send(422, {"error": message})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8013)
    ap.add_argument("--checkpoint", required=True)
    ap.add_argument("--device", choices=("cpu", "cuda"), default="cpu")
    args = ap.parse_args()

    checkpoint = Path(args.checkpoint).resolve()
    if not (checkpoint / "model.safetensors").is_file():
        raise SystemExit(f"Julia checkpoint is incomplete: {checkpoint}")
    engine = build_runtime(str(checkpoint), args.device)
    configure_handler(
        engine,
        {
            "device": args.device,
            "strict_encoding": True,
            "max_length": 8192,
            "head_length": 512,
            "marker_only_head": False,
            "weights_sha256": WEIGHTS_SHA256,
        },
    )
    print(
        f"Julia 1 ready: http://{args.host}:{args.port}/v1/systemone "
        f"device={args.device} model={MODEL}@{REVISION}",
        flush=True,
    )
    ThreadingHTTPServer((args.host, args.port), Handler).serve_forever()


if __name__ == "__main__":
    main()
