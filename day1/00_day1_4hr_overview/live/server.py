"""Live classroom server for the Day 1 deck.

Serves ../index.html on the venue network. The trainer's browser (opened with
?host=<token>) drives the slides; every participant's browser follows it and
reports votes, quiz answers, discussion ideas and game scores back over one
WebSocket. Everything is kept in memory and mirrored to live_state.json, so a
restart picks up where the class left off.

    ./day1/00_day1_4hr_overview/live/run.sh          # PORT=8000 by default
"""

import asyncio
import io
import json
import os
import re
import secrets
import socket
import sys
from collections import Counter
from contextlib import asynccontextmanager
from pathlib import Path

import segno
import uvicorn
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles

HERE = Path(__file__).resolve().parent
DECK = HERE.parent / "index.html"
ASSETS = HERE.parent / "assets"
STATE_FILE = HERE / "live_state.json"
TOKEN_FILE = HERE / ".host_token"
PORT = int(os.environ.get("PORT", "8000"))


def lan_ip():
    # Connecting a UDP socket sends nothing; it only asks the OS which interface it would use.
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))
        return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        s.close()


JOIN_URL = os.environ.get("LIVE_JOIN_URL") or f"http://{lan_ip()}:{PORT}"


def blank():
    return {"slide": 0, "people": {}, "votes": {}, "answers": {}, "totals": {}, "ideas": {}, "scores": {}}


def load():
    try:
        data = json.loads(STATE_FILE.read_text())
    except (OSError, ValueError):
        data = {}
    st = blank()
    st.update({k: v for k, v in data.items() if k in st})
    # The trainer link stays the same across restarts and resets, so it can be bookmarked.
    token = os.environ.get("LIVE_HOST_TOKEN")
    if not token:
        try:
            token = TOKEN_FILE.read_text().strip()
        except OSError:
            token = ""
    if not token:
        token = secrets.token_hex(4)
        TOKEN_FILE.write_text(token)
    return st, token


state, TOKEN = load()
hosts: set[WebSocket] = set()
guests: dict[WebSocket, str] = {}
dirty = True


def save():
    tmp = STATE_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(state))
    tmp.replace(STATE_FILE)


def clip(value, n):
    return str(value or "").strip()[:n]


def stats():
    online = set(guests.values())
    people = [
        {"name": p["name"], "online": cid in online,
         "points": sum(game.get(cid, 0) for game in state["scores"].values())}
        for cid, p in state["people"].items()
    ]
    people.sort(key=lambda p: (not p["online"], p["name"].lower()))
    acts = {}
    for act, questions in state["answers"].items():
        total = state["totals"].get(act, len(questions))
        per = {}
        for by in questions.values():
            for cid, ok in by.items():
                tally = per.setdefault(cid, [0, 0])
                tally[0] += 1
                tally[1] += bool(ok)
        answered = sum(a for a, _ in per.values())
        right = sum(r for _, r in per.values())
        acts[act] = {"people": len(per), "done": sum(1 for _, r in per.values() if r >= total),
                     "pct": round(100 * right / answered) if answered else 0}
    board = sorted((p for p in people if p["points"]), key=lambda p: -p["points"])[:10]
    return {"type": "stats", "online": len(online), "joined": len(people), "people": people,
            "votes": Counter(state["votes"].values()), "acts": acts, "board": board,
            "slide": state["slide"], "joinUrl": JOIN_URL}


async def send(ws, msg):
    try:
        await ws.send_json(msg)
    except Exception:
        pass


async def broadcast(msg, to_hosts=True):
    targets = list(guests) + (list(hosts) if to_hosts else [])
    await asyncio.gather(*(send(ws, msg) for ws in targets))


async def push_stats():
    global dirty
    while True:
        await asyncio.sleep(0.5)
        if dirty:
            dirty = False
            msg = stats()
            await asyncio.gather(*(send(ws, msg) for ws in list(hosts)))
            # Everyone gets the names (in join order) for the waiting-room slide; points stay host-only.
            online = set(guests.values())
            roster = {"type": "roster", "people": [{"name": p["name"], "online": cid in online}
                                                   for cid, p in state["people"].items()]}
            await broadcast(roster)


@asynccontextmanager
async def lifespan(_app):
    task = asyncio.create_task(push_stats())
    yield
    task.cancel()


app = FastAPI(lifespan=lifespan, docs_url=None, redoc_url=None)
app.mount("/assets", StaticFiles(directory=ASSETS), name="assets")


@app.get("/", response_class=HTMLResponse)
@app.get("/index.html", response_class=HTMLResponse)
async def deck(request: Request):
    is_host = request.query_params.get("host") == TOKEN
    cfg = {"role": "host" if is_host else "guest", "joinUrl": JOIN_URL, "token": TOKEN if is_host else None}
    html = DECK.read_text(encoding="utf-8").replace(
        "</head>", "<script>window.LIVE_CONFIG = " + json.dumps(cfg) + ";</script>\n</head>", 1)
    return HTMLResponse(html, headers={"Cache-Control": "no-store"})


@app.get("/live/qr.svg")
async def qr():
    buf = io.BytesIO()
    segno.make(JOIN_URL, error="m").save(buf, kind="svg", scale=8, border=2, dark="#05060D", light="#ffffff")
    return Response(buf.getvalue(), media_type="image/svg+xml")


async def handle(msg, is_host, cid):
    global state
    kind = msg.get("type")
    if is_host and kind == "slide":
        state["slide"] = max(0, min(999, int(msg.get("i", 0))))
        await broadcast({"type": "slide", "i": state["slide"]}, to_hosts=False)
    elif is_host and kind == "reset":
        state = {**blank(), "slide": state["slide"],
                 "people": {c: p for c, p in state["people"].items() if c in guests.values()}}
        await broadcast({"type": "reset"}, to_hosts=False)
        await broadcast({"type": "ideas", "ideas": state["ideas"]})
    elif is_host and kind == "delIdea":
        ideas = state["ideas"].get(clip(msg.get("talk"), 24), [])
        idx = int(msg.get("idx", -1))
        if 0 <= idx < len(ideas):
            ideas.pop(idx)
            await broadcast({"type": "ideas", "ideas": state["ideas"]})
    elif kind == "idea":
        text = clip(msg.get("text"), 280)
        if not text:
            return
        tag = re.sub(r"[^A-Z0-9 _-]", "", clip(msg.get("tag"), 16).upper()) or "IDEA"
        name = "Trainer" if is_host else state["people"].get(cid, {}).get("name", "Guest")
        state["ideas"].setdefault(clip(msg.get("talk"), 24), []).append({"t": text, "g": tag, "n": name})
        await broadcast({"type": "ideas", "ideas": state["ideas"]})
    elif is_host:
        return
    elif kind == "hello":
        state["people"][cid] = {"name": clip(msg.get("name"), 24) or "Guest"}
    elif kind == "vote" and msg.get("vote") in ("A", "B", "C"):
        state["votes"][cid] = msg["vote"]
    elif kind == "answer":
        act = clip(msg.get("activity"), 32)
        state["answers"].setdefault(act, {}).setdefault(clip(msg.get("q"), 200), {})[cid] = bool(msg.get("ok"))
        state["totals"][act] = max(1, min(50, int(msg.get("total", 1))))
    elif kind == "score":
        game = state["scores"].setdefault(clip(msg.get("game"), 32), {})
        game[cid] = max(game.get(cid, 0), max(0, min(100000, int(msg.get("score", 0)))))
    else:
        return
    save()


@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    global dirty
    await ws.accept()
    is_host = ws.query_params.get("host") == TOKEN
    cid = clip(ws.query_params.get("id"), 40) or secrets.token_hex(6)
    if is_host:
        hosts.add(ws)
    else:
        guests[ws] = cid
        state["people"].setdefault(cid, {"name": "Guest"})
    await send(ws, {"type": "slide", "i": state["slide"]})
    await send(ws, {"type": "ideas", "ideas": state["ideas"]})
    dirty = True
    try:
        while True:
            try:
                msg = json.loads(await ws.receive_text())
                await handle(msg, is_host, cid)
            except (ValueError, TypeError, AttributeError):
                continue
            dirty = True
    except WebSocketDisconnect:
        pass
    finally:
        hosts.discard(ws)
        guests.pop(ws, None)
        dirty = True


if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        try:
            probe.bind(("0.0.0.0", PORT))
        except OSError:
            raise SystemExit(f"""
  ✖ Port {PORT} is already in use (often a leftover `python3 -m http.server {PORT}`).
    See what holds it:   lsof -nP -iTCP:{PORT} -sTCP:LISTEN
    Stop that program (Ctrl+C in its terminal, or kill <PID>), or pick another port:
    PORT=8080 {sys.argv[0]}
""")
    print(f"""
  ▶ DAY 1 LIVE · serving {DECK.name}
    Participants : {JOIN_URL}          (QR code on slide 1)
    Trainer      : {JOIN_URL}/?host={TOKEN}   <- keep this one private
    Local test   : http://localhost:{PORT}/?host={TOKEN}
    State file   : {STATE_FILE}
                   Use Reset in the Control Center (key C) for a fresh class.
""")
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="warning")
