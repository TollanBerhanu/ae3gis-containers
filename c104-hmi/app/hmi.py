#!/usr/bin/env python3
"""IEC-104 operator console (HMI) for the AE3GIS lab (Scenario B).

Connects to the RTU (the c104-server image) as an IEC-104 client, tracks the
breaker state via periodic general interrogation, and serves a small web console
on :8080 that shows the breaker state and offers open/close controls.

The c104 client setup runs in a retrying background thread (c104 needs a numeric
IP, and the RTU may not be up yet), so the web view always stays up. Educational,
isolated-lab use.
"""
import os
import socket
import threading
import time

import c104
from flask import Flask, redirect

SERVER = os.environ.get("IEC104_SERVER", "c104-server")
PORT = int(os.environ.get("IEC104_PORT", "2404"))
WEB_PORT = int(os.environ.get("HMI_WEB_PORT", "8080"))
COMMON_ADDRESS = int(os.environ.get("IEC104_COMMON_ADDRESS", "47"))
STATE_IOA = int(os.environ.get("BREAKER_STATE_IOA", "11"))
CMD_IOA = int(os.environ.get("BREAKER_CMD_IOA", "12"))

_lock = threading.Lock()
_ctx = {"command": None, "breaker": None, "connection": None}


def _resolve(host: str) -> str:
    """Return host as an IP, retrying while DNS/hosts is not ready yet."""
    while True:
        try:
            return socket.gethostbyname(host)
        except OSError:
            time.sleep(2)


def worker() -> None:
    client = c104.Client()
    connection = client.add_connection(ip=_resolve(SERVER), port=PORT)
    station = connection.add_station(common_address=COMMON_ADDRESS)
    breaker = station.add_point(io_address=STATE_IOA, type=c104.Type.M_SP_NA_1)
    command = station.add_point(io_address=CMD_IOA, type=c104.Type.C_SC_NA_1)
    with _lock:
        _ctx.update(command=command, breaker=breaker, connection=connection)
    client.start()
    while True:
        try:
            if connection.is_connected:
                connection.interrogation(common_address=COMMON_ADDRESS)
        except Exception:
            pass
        time.sleep(2)


threading.Thread(target=worker, daemon=True).start()

app = Flask(__name__)

# A small dark console: one clear state panel and the open/close controls.
# No external assets (the page is relayed through the backend's web-UI proxy),
# so styling is inline. Dynamic values are substituted with str.replace to keep
# the CSS brace-free.
PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Substation Breaker</title>
<meta http-equiv="refresh" content="2">
<style>
  *{box-sizing:border-box}
  body{margin:0;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:20px;
    background:#0b1118;color:#dfe8f3;font-family:"Segoe UI",system-ui,-apple-system,sans-serif}
  .card{width:100%;max-width:300px;background:#121a24;border:1px solid #223042;border-radius:14px;
    padding:20px;text-align:center;box-shadow:0 16px 44px rgba(0,0,0,.5)}
  .title{font-size:11px;color:#7d8ea3;text-transform:uppercase;letter-spacing:.18em;font-weight:700}
  .panel{margin:16px 0;padding:22px 16px;border-radius:12px;border:1px solid var(--c);
    background:var(--bg);display:flex;flex-direction:column;align-items:center;gap:8px}
  .panel svg{width:40px;height:40px}
  .label{font-size:26px;font-weight:800;letter-spacing:.06em;color:var(--c)}
  .sub{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:#7d8ea3}
  .p-closed{--c:#2fd27a;--bg:rgba(47,210,122,.10)}
  .p-open{--c:#ff5a5a;--bg:rgba(255,90,90,.10)}
  .p-unknown{--c:#9fb0c3;--bg:rgba(125,142,163,.08)}
  .controls{display:grid;grid-template-columns:1fr 1fr;gap:10px}
  button{font:inherit;font-weight:700;font-size:13px;letter-spacing:.06em;text-transform:uppercase;cursor:pointer;
    padding:11px;border-radius:9px;border:1px solid #223042;color:#dfe8f3;background:#182230;
    transition:filter .12s,transform .02s}
  button:hover{filter:brightness(1.16)}
  button:active{transform:translateY(1px)}
  .btn-close{border-color:rgba(47,210,122,.4);color:#8ff0c0;background:#132a20}
  .btn-open{border-color:rgba(255,90,90,.4);color:#ffb0b0;background:#2a1417}
  form{margin:0}
  .foot{margin-top:14px;font-size:10px;color:#6b7a90;font-family:"Consolas",ui-monospace,monospace;letter-spacing:.03em}
</style>
</head>
<body>
  <div class="card">
    <div class="title">Substation Breaker · CB-52</div>
    <div class="panel p-__DKEY__">
      __GLYPH__
      <div class="label">__LABEL__</div>
      <div class="sub">__SUB__</div>
    </div>
    <div class="controls">
      <form method="post" action="/close"><button class="btn-close" type="submit" style="width:100%">Close</button></form>
      <form method="post" action="/open"><button class="btn-open" type="submit" style="width:100%">Open</button></form>
    </div>
    <div class="foot">RTU __CONN__ · __TS__</div>
  </div>
</body>
</html>"""


def _glyph(state: str) -> str:
    """A small breaker-contact symbol: closed = contacts joined, open = parted."""
    c = {"closed": "#2fd27a", "open": "#ff5a5a", "unknown": "#9fb0c3"}[state]
    if state == "closed":
        contact = f'<line x1="24" y1="14" x2="24" y2="34" stroke="{c}" stroke-width="3.5" stroke-linecap="round"/>'
    elif state == "open":
        contact = f'<line x1="24" y1="14" x2="12" y2="26" stroke="{c}" stroke-width="3.5" stroke-linecap="round"/>'
    else:
        contact = f'<line x1="24" y1="14" x2="15" y2="25" stroke="{c}" stroke-width="3.5" stroke-linecap="round" stroke-dasharray="3 3"/>'
    return (
        f'<svg viewBox="0 0 48 48" role="img" aria-hidden="true">'
        f'<line x1="24" y1="2" x2="24" y2="14" stroke="{c}" stroke-width="3.5"/>'
        f'<line x1="24" y1="34" x2="24" y2="46" stroke="{c}" stroke-width="3.5"/>'
        f'<circle cx="24" cy="14" r="3.5" fill="{c}"/>'
        f'<circle cx="24" cy="34" r="3.5" fill="{c}"/>'
        f'{contact}</svg>'
    )


def send(value: bool) -> None:
    with _lock:
        command = _ctx["command"]
    if command is None:
        return
    try:
        command.value = value
        command.transmit(cause=c104.Cot.ACTIVATION)
    except Exception as exc:  # keep the console alive regardless
        print(f"[c104-hmi] command failed: {exc}", flush=True)


@app.route("/")
def index() -> str:
    with _lock:
        breaker = _ctx["breaker"]
        connection = _ctx["connection"]
    val = breaker.value if breaker is not None else None
    if val is True:
        dkey, label, sub = "closed", "CLOSED", "energized"
    elif val is False:
        dkey, label, sub = "open", "OPEN", "de-energized"
    else:
        dkey, label, sub = "unknown", "UNKNOWN", "awaiting RTU"

    conn = "connecting"
    if connection is not None:
        conn = "connected" if connection.is_connected else "disconnected"

    repl = {
        "__DKEY__": dkey,
        "__GLYPH__": _glyph(dkey),
        "__LABEL__": label,
        "__SUB__": sub,
        "__CONN__": conn,
        "__TS__": time.strftime("%H:%M:%S"),
    }
    page = PAGE
    for key, value in repl.items():
        page = page.replace(key, value)
    return page


@app.route("/open", methods=["POST"])
def open_breaker():
    send(False)
    return redirect("/")


@app.route("/close", methods=["POST"])
def close_breaker():
    send(True)
    return redirect("/")


print(f"[c104-hmi] web console on :{WEB_PORT}, RTU {SERVER}:{PORT}", flush=True)
app.run(host="0.0.0.0", port=WEB_PORT)
