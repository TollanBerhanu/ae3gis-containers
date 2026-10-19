# IEC-104 RTU (c104-server) Container

## Overview
An IEC 60870-5-104 (IEC-104) **RTU** acting as the substation field device in Scenario B. Built on the `c104` Python library, it exposes a single breaker on TCP **2404**. Classified in AE3GIS as a `plc` (field device) variant.

## Features
- Ubuntu 24.04 LTS base image
- IEC-104 server on TCP 2404 (`c104`, in a venv at `/opt/venv`)
- One breaker: a monitored single-point (state) and a single-command point (open/close)
- A received command is mirrored onto the state point, so an HMI sees the change
- SSH access (`root:pass`)

## The breaker (defaults, override via env)
| Env | Default | Meaning |
|---|---|---|
| `IEC104_PORT` | `2404` | listen port |
| `IEC104_COMMON_ADDRESS` | `47` | IEC-104 common address |
| `BREAKER_STATE_IOA` | `11` | monitored point (M_SP_NA_1): breaker state |
| `BREAKER_CMD_IOA` | `12` | command point (C_SC_NA_1): open/close |

The server starts with the breaker **closed**.

## Usage
```bash
# the RTU starts automatically (CMD); check it is listening
ss -ltn | grep 2404
```
Point an IEC-104 client (the `c104-hmi` image, or a scenario script) at this node's address on 2404 to read and control the breaker. The app is `/opt/app/server.py`.

> Credentials and SSH settings are intentionally weak for an isolated lab. Never reuse outside one.
