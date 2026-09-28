#!/usr/bin/env python3
"""Thin System One HTTP transport around SemIf's unmodified direct scorer."""
from __future__ import annotations

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import argparse, json, platform, sys, threading, time

MODEL = "Qwen/Qwen3.5-4B"
REVISION = "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
_lock = threading.Lock()


def _question_to_row(state, qid, q):
    kind = str(q.get("type", "")).lower()
    criterion = q.get("instructions", "")
    criteria = q.get("criteria")
    if kind == "choice":
        raw = criteria or q.get("options") or q.get("choices") or {}
        if isinstance(raw, dict):
            opts = [{"id": str(k), "description": str(v)} for k, v in raw.items()]
        else:
            opts = [{"id": str(x.get("id", i)), "description": str(x.get("description", x.get("label", x)))} for i, x in enumerate(raw)]
    elif kind in ("noul", "bool", "boolean"):
        opts = [{"id": "false", "description": "No; the criterion is false."}, {"id": "true", "description": "Yes; the criterion is true."}]
    elif kind in ("score", "scale"):
        levels = criteria or q.get("levels") or q.get("legend") or q.get("options") or []
        if isinstance(levels, dict):
            opts = [{"id": str(k), "description": str(v)} for k, v in levels.items()]
        else:
            opts = [{"id": str(i), "description": str(v)} for i, v in enumerate(levels)]
    else:
        raise ValueError(f"unsupported question type: {kind!r}")
    if not 2 <= len(opts) <= 16:
        raise ValueError(f"SemIf supports 2-16 options; got {len(opts)}")
    return {"id": str(qid), "state": state, "question": str(criterion), "options": opts}, kind, opts


def _answer(kind, opts, result):
    probs = [float(x) for x in result["probabilities"]]
    by_id = {str(opt["id"]): p for opt, p in zip(opts, probs)}
    best = max(range(len(probs)), key=probs.__getitem__)
    if kind == "choice":
        return {"type": "choice", "choice": str(opts[best]["id"]), "probabilities": by_id}
    if kind in ("noul", "bool", "boolean"):
        return {"type": "noul", "noul": by_id["true"], "probabilities": by_id}
    numeric = []
    for opt in opts:
        try: numeric.append(float(opt["id"]))
        except ValueError: numeric.append(float(len(numeric)))
    score = sum(v * p for v, p in zip(numeric, probs))
    return {"type": "score", "score": score, "probabilities": by_id}


def build_runtime(device: str):
    from semif_phase1.core import load_causal_model
    from semif_phase1.direct import score
    kwargs = {}
    if device == "cpu": kwargs["dtype"] = "float32"
    model, tokenizer, metadata = load_causal_model(MODEL, REVISION, device, **kwargs)
    def decide(row):
        with _lock:
            return score(model, tokenizer, row, metadata, 4096)
    return decide, metadata


def configure_handler(decide, metadata):
    # Functions assigned directly to a class are descriptors and become bound
    # methods when accessed through ``self``.  SemIf's runtime callback accepts
    # only the benchmark row, so keep it static to prevent ``self`` injection.
    Handler.decide = staticmethod(decide)
    Handler.metadata = metadata


class Handler(BaseHTTPRequestHandler):
    decide = None
    metadata = None
    def log_message(self, fmt, *args):
        return
    def _send(self, status, body):
        data = json.dumps(body, allow_nan=False).encode()
        self.send_response(status); self.send_header("Content-Type", "application/json"); self.send_header("Content-Length", str(len(data))); self.end_headers(); self.wfile.write(data)
    def do_GET(self):
        if self.path == "/health": self._send(200, {"status":"ok", "model":MODEL, "revision":REVISION, "metadata":self.metadata})
        else: self._send(404, {"error":"not found"})
    def do_POST(self):
        if self.path != "/v1/systemone": return self._send(404, {"error":"not found"})
        try:
            n=int(self.headers.get("Content-Length","0")); payload=json.loads(self.rfile.read(n)); started=time.perf_counter(); answers={}
            for qid, q in payload.get("questions", {}).items():
                row, kind, opts = _question_to_row(payload.get("state"), qid, q)
                answers[str(qid)] = _answer(kind, opts, self.decide(row))
            self._send(200, {"model":f"SemIf:{MODEL}@{REVISION}", "provider":"semif", "answers":answers, "elapsed_ms":(time.perf_counter()-started)*1000.0, "usage":{"output_tokens":0}})
        except Exception as exc:
            message = f"{type(exc).__name__}: {exc}"
            print(f"SemIf request failed: {message}", file=sys.stderr, flush=True)
            self._send(422, {"error": message})


def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--host",default="127.0.0.1"); ap.add_argument("--port",type=int,default=8012); ap.add_argument("--device",default="auto"); args=ap.parse_args()
    device=args.device
    if device == "auto": device="mps" if platform.system()=="Darwin" and platform.machine()=="arm64" else "cuda"
    decide, metadata = build_runtime(device)
    configure_handler(decide, metadata)
    print(f"SemIf ready: http://{args.host}:{args.port}/v1/systemone device={device} model={MODEL}@{REVISION}", flush=True)
    ThreadingHTTPServer((args.host,args.port), Handler).serve_forever()
if __name__ == "__main__": main()
