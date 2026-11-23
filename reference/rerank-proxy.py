#!/usr/bin/env python3
"""Loopback /rerank endpoint for OpenClaw's rerank Decision provider.

llama.cpp's --rerank server returns raw logits for cross-encoder rerankers
(BGE, GTE, Jina). OpenClaw rejects scores outside 0..1 and warns against
rescaling per batch, so this proxy applies a fixed per-model sigmoid.
Models that already return probabilities (Qwen3-Reranker) pass through.

Listens on 127.0.0.1:8094, forwards to llama-server --rerank on 127.0.0.1:8095.
"""
import json
import math
import os
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

UPSTREAM = os.environ.get("RERANK_UPSTREAM", "http://127.0.0.1:8095")
LISTEN = int(os.environ.get("RERANK_PORT", "8094"))
# "sigmoid" for logit-output cross-encoders, "none" for probability output
SCORE_MODE = os.environ.get("RERANK_SCORE_MODE", "sigmoid")


def sig(x):
    if x >= 0:
        return 1 / (1 + math.exp(-x))
    e = math.exp(x)
    return e / (1 + e)


class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _send(self, code, obj):
        b = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_GET(self):
        if self.path.rstrip("/") in ("/health", "/v1/models", "/models"):
            try:
                with urllib.request.urlopen(UPSTREAM + self.path, timeout=10) as r:
                    return self._send(r.status, json.loads(r.read()))
            except Exception as e:
                return self._send(503, {"error": str(e)})
        self._send(404, {"error": "not found"})

    def do_POST(self):
        if self.path.rstrip("/") not in ("/rerank", "/v1/rerank"):
            return self._send(404, {"error": "not found"})
        try:
            req = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))))
            docs = req.get("documents") or req.get("texts") or []
            up = {"query": req.get("query", ""), "documents": docs}
            if "top_n" in req:
                up["top_n"] = req["top_n"]
            r = urllib.request.Request(UPSTREAM + "/v1/rerank", data=json.dumps(up).encode(),
                                       headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(r, timeout=300) as resp:
                d = json.loads(resp.read())
            res = []
            for x in d.get("results", []):
                s = x["relevance_score"]
                if SCORE_MODE == "sigmoid":
                    s = sig(s)
                res.append({"index": x["index"], "relevance_score": min(1.0, max(0.0, s))})
            res.sort(key=lambda x: -x["relevance_score"])
            self._send(200, {"model": req.get("model", ""), "results": res,
                             "usage": d.get("usage", {})})
        except Exception as e:
            self._send(502, {"error": str(e)})


if __name__ == "__main__":
    ThreadingHTTPServer(("127.0.0.1", LISTEN), H).serve_forever()
