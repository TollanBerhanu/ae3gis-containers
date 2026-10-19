#!/usr/bin/env python3
"""Minimal IEC-104 RTU for the AE3GIS lab (Scenario B).

Exposes a single substation breaker on TCP 2404:
  - a monitored single-point (M_SP_NA_1) carrying the breaker state, and
  - a single-command point (C_SC_NA_1) that opens/closes it.

A received command is mirrored onto the state point so an HMI sees the change.
Addresses are overridable by environment variable. Educational, isolated-lab use.
"""
import os
import signal
import time

import c104

PORT = int(os.environ.get("IEC104_PORT", "2404"))
COMMON_ADDRESS = int(os.environ.get("IEC104_COMMON_ADDRESS", "47"))
STATE_IOA = int(os.environ.get("BREAKER_STATE_IOA", "11"))
CMD_IOA = int(os.environ.get("BREAKER_CMD_IOA", "12"))

server = c104.Server(ip="0.0.0.0", port=PORT)
station = server.add_station(common_address=COMMON_ADDRESS)

breaker = station.add_point(io_address=STATE_IOA, type=c104.Type.M_SP_NA_1)
breaker.value = True  # start closed

command = station.add_point(io_address=CMD_IOA, type=c104.Type.C_SC_NA_1)


def on_command(point: c104.Point, previous_info: c104.Information,
               message: c104.IncomingMessage) -> c104.ResponseState:
    breaker.value = bool(point.value)
    print(f"[c104-server] breaker -> {'CLOSED' if point.value else 'OPEN'}", flush=True)
    return c104.ResponseState.SUCCESS


command.on_receive(callable=on_command)

server.start()
print(f"[c104-server] IEC-104 RTU listening on :{PORT} "
      f"(CA={COMMON_ADDRESS}, state IOA={STATE_IOA}, command IOA={CMD_IOA})",
      flush=True)

signal.signal(signal.SIGTERM, lambda *_: os._exit(0))
while True:
    time.sleep(1)
