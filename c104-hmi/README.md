# IEC-104 HMI (c104-hmi) Container

## Overview
An IEC-104 operator console for Scenario B. It connects to the RTU (the `c104-server` image) as an IEC-104 client, tracks the breaker state, and serves a small web page on **8080** that shows the state and offers open/close controls. Classified in AE3GIS as an `hmi` variant.

## Features
- Ubuntu 24.04 LTS base image
- IEC-104 client + Flask web console (`c104`, `flask` in a venv at `/opt/venv`)
- Web page on port 8080, auto-refreshing, with Close/Open buttons
- Reconnects on its own; stays up even if the RTU is not reachable yet
- SSH access (`root:pass`)

## Configuration (env)
| Env | Default | Meaning |
|---|---|---|
| `IEC104_SERVER` | `c104-server` | RTU hostname/IP to connect to |
| `IEC104_PORT` | `2404` | RTU port |
| `HMI_WEB_PORT` | `8080` | web console port |
| `IEC104_COMMON_ADDRESS` | `47` | IEC-104 common address |
| `BREAKER_STATE_IOA` / `BREAKER_CMD_IOA` | `11` / `12` | breaker point addresses (match the RTU) |

## Usage
```bash
# browse to the console
curl -s http://<node-ip>:8080/ | head
```
Set `IEC104_SERVER` to the RTU's address in the topology. The app is `/opt/app/hmi.py`.

> Credentials and SSH settings are intentionally weak for an isolated lab. Never reuse outside one.
