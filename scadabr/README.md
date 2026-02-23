# ScadaBR Container

## Overview

This container provides [ScadaBR](https://github.com/ScadaBR/ScadaBR), an open-source SCADA (Supervisory Control and Data Acquisition) system. It is used for monitoring and controlling industrial processes, and it integrates well with OpenPLC and other Modbus-capable devices for ICS security labs.

> **Status:** Experimental — the current Dockerfile clones the ScadaBR installer repository. A manual installation step is required inside the running container before ScadaBR is fully operational.

## Features

- Ubuntu 24.04 LTS base image
- ScadaBR installer cloned at build time
- Web interface on port 8080 (after installation)
- Designed to pair with the `openplc` container over Modbus TCP

## Prerequisites

The ScadaBR installer expects to run interactively. After building and starting the container you must complete the installation manually (see below).

## Usage in GNS3

### Building the Image

```bash
docker build -t ae3gis-scadabr ./scadabr/
```

### Starting the Container

1. Import the image into GNS3 (see the [central README](../README.md) for the step-by-step guide).
2. Connect to at least one network interface.
3. Start the container and open a console.

### Completing the Installation

Inside the running container:

```bash
cd /ScadaBR_Installer
# Follow the interactive prompts — the defaults are usually fine
./install.sh
```

> After installation, you may want to commit the modified container as a new Docker image so you don't have to repeat this step:
> ```bash
> # From the Docker host (not inside the container)
> docker commit <container_id> ae3gis-scadabr:installed
> ```

### Starting ScadaBR

After installation (assuming you kept the default paths):

```bash
./ScadaBR_Installer/scadabr.sh start
```

Then open a browser and navigate to:

```
http://<container_ip>:8080/ScadaBR
```

Default credentials: **admin** / **admin**

## Ports

| Port | Protocol | Service |
|------|----------|---------|
| 8080 | TCP      | ScadaBR web interface |

## Integration with OpenPLC

ScadaBR can communicate with an OpenPLC container over Modbus TCP. In the ScadaBR web UI:

1. Go to **Data Sources → Add → Modbus IP**.
2. Set the **Host** to the OpenPLC container's IP address and **Port** to `502`.
3. Add data points that correspond to the Modbus registers exposed by your PLC program.

## Logging

- ScadaBR application logs are available inside the web interface under **System Information**.
- System logs (if rsyslog is installed): `/var/log/syslog`

## Known Limitations

- The Dockerfile currently only clones the installer — it does **not** run the installation automatically because the installer is interactive.
- No SSH server or standard baseline packages are installed yet. This container departs from the repository-wide conventions.
- Future improvements may automate the installation step so the container is ready to use immediately.

## Troubleshooting

- **`install.sh` fails:** Make sure the container has internet access during installation so dependencies can be downloaded.
- **Web interface not loading:** Ensure ScadaBR was started with `scadabr.sh start` and that port 8080 is reachable.
- **Cannot connect to OpenPLC:** Verify the OpenPLC container is running, the PLC program is started, and the Modbus data source IP/port are correct in ScadaBR.