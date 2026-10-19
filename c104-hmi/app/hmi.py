#!/usr/bin/env python3
"""IEC-104 operator console (HMI) for the AE3GIS lab (Scenario B).

Connects to the RTU (the c104-server image) as an IEC-104 client, tracks the
breaker state via periodic general interrogation, and serves a minimal web page
on :8080 that shows the state and offers open/close controls.

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

PAGE = """<!doctype html><html><head><meta charset="utf-8">
<title>IEC-104 HMI</title><meta http-equiv="refresh" content="3">
<style>body{{font-family:system-ui,sans-serif;max-width:40ch;margin:3rem auto;text-align:center}}
.state{{font-size:2rem;font-weight:700;padding:1rem;border-radius:.5rem;margin:1rem 0}}
.closed{{background:#1b5e20;color:#fff}}.open{{background:#b71c1c;color:#fff}}
.unknown{{background:#555;color:#fff}}button{{font-size:1rem;padding:.6rem 1.4rem;margin:.3rem}}</style>
</head><body><h1>Substation breaker</h1>
<div class="state {cls}">{label}</div>
<form method="post" action="/close"><button>Close</button></form>
<form method="post" action="/open"><button>Open</button></form>
<p><small>RTU {server}:{port} · {conn}</small></p>
</body></html>"""


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
        cls, label = "closed", "CLOSED"
    elif val is False:
        cls, label = "open", "OPEN"
    else:
        cls, label = "unknown", "UNKNOWN"
    conn = "connecting"
    if connection is not None:
        conn = "connected" if connection.is_connected else "disconnected"
    return PAGE.format(cls=cls, label=label, server=SERVER, port=PORT, conn=conn)


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
