#!/usr/bin/env python3
"""Physical-process simulator + projector view for the AE3GIS lab.

Polls the field device's true output and shows it on a big web page (:8000),
so a demo can project the real process state next to the HMI. One image serves
both scenarios, chosen by SIM_PROTO:
  - modbus : read a register/coil from the PLC (OpenPLC, Scenario A)
  - iec104 : read the breaker point from the RTU (c104-server, Scenario B)

Built to stay up: every poll is guarded, and the view keeps the last known value
and marks it stale rather than crashing. Educational, isolated-lab use.
"""
import os
import socket
import threading
import time

from flask import Flask

PROTO = os.environ.get("SIM_PROTO", "modbus").lower()
WEB_PORT = int(os.environ.get("SIM_WEB_PORT", "8000"))
FIELD_HOST = os.environ.get("FIELD_HOST", "openplc")
POLL_SECONDS = float(os.environ.get("SIM_POLL_SECONDS", "2"))

# Modbus (Scenario A) knobs
MODBUS_PORT = int(os.environ.get("FIELD_PORT", "502"))
MODBUS_ADDRESS = int(os.environ.get("MODBUS_ADDRESS", "0"))
MODBUS_KIND = os.environ.get("MODBUS_KIND", "holding")  # holding | coil

# IEC-104 (Scenario B) knobs
IEC104_PORT = int(os.environ.get("FIELD_PORT", "2404"))
IEC104_COMMON_ADDRESS = int(os.environ.get("IEC104_COMMON_ADDRESS", "47"))
IEC104_STATE_IOA = int(os.environ.get("BREAKER_STATE_IOA", "11"))

_lock = threading.Lock()
_state = {"value": None, "updated": 0.0, "ok": False}


def _set(value, ok: bool) -> None:
    with _lock:
        if value is not None:
            _state["value"] = value
        _state["ok"] = ok
        if ok:
            _state["updated"] = time.time()


def poll_modbus() -> None:
    from pymodbus.client import ModbusTcpClient

    client = ModbusTcpClient(host=FIELD_HOST, port=MODBUS_PORT)
    while True:
        try:
            client.connect()
            if MODBUS_KIND == "coil":
                rr = client.read_coils(MODBUS_ADDRESS, count=1)
                value = None if rr.isError() else bool(rr.bits[0])
            else:
                rr = client.read_holding_registers(MODBUS_ADDRESS, count=1)
                value = None if rr.isError() else int(rr.registers[0])
            _set(value, value is not None)
        except Exception:
            _set(None, False)
        time.sleep(POLL_SECONDS)


def _resolve(host: str) -> str:
    """Return host as an IP, retrying while DNS/hosts is not ready yet (c104 needs a numeric IP)."""
    while True:
        try:
            return socket.gethostbyname(host)
        except OSError:
            time.sleep(POLL_SECONDS)


def poll_iec104() -> None:
    import c104

    client = c104.Client()
    connection = client.add_connection(ip=_resolve(FIELD_HOST), port=IEC104_PORT)
    station = connection.add_station(common_address=IEC104_COMMON_ADDRESS)
    point = station.add_point(io_address=IEC104_STATE_IOA, type=c104.Type.M_SP_NA_1)
    client.start()
    while True:
        try:
            if connection.is_connected:
                connection.interrogation(common_address=IEC104_COMMON_ADDRESS)
                val = point.value
                _set(None if val is None else bool(val), val is not None)
            else:
                _set(None, False)
        except Exception:
            _set(None, False)
        time.sleep(POLL_SECONDS)


app = Flask(__name__)

PAGE = """<!doctype html><html><head><meta charset="utf-8">
<title>Process view</title><meta http-equiv="refresh" content="2">
<style>body{{font-family:system-ui,sans-serif;margin:0;height:100vh;display:flex;
flex-direction:column;align-items:center;justify-content:center;background:#0b1021;color:#e8eaf6}}
.v{{font-size:22vmin;font-weight:800;line-height:1}}
.meta{{margin-top:2rem;font-size:1.2rem;color:#9fa8da}}
.stale{{color:#ff8a80}}</style></head><body>
<div class="v">{value}</div>
<div class="meta {stalecls}">{proto} · {host} · {freshness}</div>
</body></html>"""


@app.route("/")
def index() -> str:
    with _lock:
        value, updated, ok = _state["value"], _state["updated"], _state["ok"]
    shown = "—" if value is None else ("CLOSED" if value is True
                                       else "OPEN" if value is False else str(value))
    if not updated:
        freshness, stalecls = "no data yet", "stale"
    else:
        age = time.time() - updated
        fresh = ok and age < POLL_SECONDS * 3
        freshness = "live" if fresh else f"stale ({int(age)}s)"
        stalecls = "" if fresh else "stale"
    target = f"{FIELD_HOST}:{MODBUS_PORT if PROTO == 'modbus' else IEC104_PORT}"
    return PAGE.format(value=shown, proto=PROTO, host=target,
                       freshness=freshness, stalecls=stalecls)


if PROTO == "iec104":
    threading.Thread(target=poll_iec104, daemon=True).start()
else:
    threading.Thread(target=poll_modbus, daemon=True).start()

print(f"[process-sim] {PROTO} view on :{WEB_PORT}, field device {FIELD_HOST}", flush=True)
app.run(host="0.0.0.0", port=WEB_PORT)
