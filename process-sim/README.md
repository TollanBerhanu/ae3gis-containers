# Process Simulator (process-sim) Container

## Overview
The physical-process simulator and **projector view** for the ICS lab. It polls the field device's true output and shows it on a large, auto-refreshing web page on port **8000**, so a demo can project the real process state next to the HMI. One image serves both scenarios, chosen by an env var. Classified in AE3GIS as a `workstation` variant (a Linux host with a web view on the OT LAN).

## Features
- Ubuntu 24.04 LTS base image
- Flask projector view on port 8000 (`flask`, `pymodbus`, `c104` in a venv at `/opt/venv`)
- Dual protocol: reads **Modbus** (Scenario A) or **IEC-104** (Scenario B)
- Resilient polling: keeps the last value and marks it stale rather than crashing
- SSH access (`root:pass`)

## Configuration (env)
| Env | Default | Meaning |
|---|---|---|
| `SIM_PROTO` | `modbus` | `modbus` (Scenario A) or `iec104` (Scenario B) |
| `FIELD_HOST` | `openplc` | field device hostname/IP |
| `FIELD_PORT` | `502` / `2404` | field device port (Modbus / IEC-104) |
| `MODBUS_ADDRESS` / `MODBUS_KIND` | `0` / `holding` | which Modbus register/coil to read |
| `BREAKER_STATE_IOA` / `IEC104_COMMON_ADDRESS` | `11` / `47` | IEC-104 point to read |
| `SIM_WEB_PORT` | `8000` | projector view port |

## Usage
```bash
# Scenario A (Modbus / OpenPLC):
#   SIM_PROTO=modbus  FIELD_HOST=<plc-ip>  FIELD_PORT=502
# Scenario B (IEC-104 RTU):
#   SIM_PROTO=iec104  FIELD_HOST=<rtu-ip>  FIELD_PORT=2404
curl -s http://<node-ip>:8000/ | head
```
The app is `/opt/app/sim.py`.

> Credentials and SSH settings are intentionally weak for an isolated lab. Never reuse outside one.
