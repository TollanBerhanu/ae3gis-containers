# AE3GIS image standard (v1)

How to publish container images on Docker Hub so AE3GIS can load them as node
images and node types. You build the image as usual and add a few labels. You
mark the Docker Hub repo for AE3GIS. A user then adds your namespace in AE3GIS
(**Images → Add registry**, e.g. `https://hub.docker.com/u/<namespace>`), and
your images appear in the palette, the type picker and the image picker.

Nothing about the image itself changes: AE3GIS runs your image's own `CMD`/
`ENTRYPOINT` and configures addressing with a boot script, as it does for every
node (see "What AE3GIS does with your image" below).

## In short

1. Start the repo's Docker Hub **short description** with `[ae3gis]`.
2. Add `io.ae3gis.schema="1"` and `io.ae3gis.type="<type id>"` labels to the image.
3. If the type is new, also label its name and role (`io.ae3gis.type.name`,
   `io.ae3gis.type.role`).
4. Push `latest`. Publishing both `linux/amd64` and `linux/arm64` is recommended.

## 1. Opting in: the repo description marker

A namespace may hold any number of images; AE3GIS only looks at repos whose
Docker Hub **short description starts with `[ae3gis]`** (any case; the rest is
free text, e.g. `[ae3gis] OpenSSH jump host`). Other repos are listed as
*skipped* and never inspected.

The marker exists because reading an image's labels costs a Docker Hub pull
(see "Rate limits" below); the description is free to read. Set it on the repo
page on Docker Hub (or with the Hub API in CI). Private repos are skipped:
AE3GIS reads Docker Hub anonymously.

## 2. One repo is one image, one tag is one version

- Each repo is one image, i.e. one *variant* of a node type. Several repos can
  be variants of the same type.
- AE3GIS reads the `latest` tag, or the most recently pushed tag if there is no
  `latest`. The node image it deploys is `<namespace>/<repo>:<tag>`.
- Repo names are never interpreted. Name them for people (e.g.
  `web-server-nginx`, `plc-openplc`); renaming one changes nothing but the ref.

## 3. Labels

Labels go in the Dockerfile (`LABEL key="value"`) and are read from the
image's config, so they travel with the image and are versioned with each tag.

### Required

| Label | Value |
|---|---|
| `io.ae3gis.schema` | `1`. Images without it are rejected; other values are rejected as unsupported. |
| `io.ae3gis.type` | The node type this image is a variant of: a lowercase id (`^[a-z][a-z0-9-]{0,39}$`), e.g. `plc`, `web-server`, `bastion`. |

### About the image (optional)

| Label | Value | Default |
|---|---|---|
| `org.opencontainers.image.title` | Display name of this variant | the repo name |
| `org.opencontainers.image.description` | One line about it | empty |
| `io.ae3gis.stability` | `stable` or `experimental` (shown as a badge) | `stable` |
| `io.ae3gis.shell` | Absolute path of the shell for boot commands, for images **without bash** (Alpine, BusyBox): `/bin/sh` | bash |
| `io.ae3gis.own-bridge` | For a switch image that bridges its own ports (e.g. Open vSwitch): the bridge's interface name, e.g. `br0`. AE3GIS then only addresses it. | AE3GIS bridges |
| `io.ae3gis.default` | `true`: this image is its **new** type's default and supplies the type's metadata | |

Base images often set `org.opencontainers.image.title`/`description` themselves
(e.g. an image `FROM` an upstream project inherits *its* title). Set both
explicitly, or your variant shows up under the upstream project's name.

### About a new type (optional, read from the type's default image)

| Label | Value | Default |
|---|---|---|
| `io.ae3gis.type.name` | Display name, e.g. `Bastion Host` | **required for a new type** |
| `io.ae3gis.type.role` | `router`, `switch` or `host`: how AE3GIS configures the node (see below) | **required for a new type** |
| `io.ae3gis.type.label` | Short badge, 1–5 characters, e.g. `BS` | first 4 letters of the id |
| `io.ae3gis.type.color` | Accent color `#rrggbb` | neutral grey |
| `io.ae3gis.type.icon` | One of `router`, `switch`, `firewall`, `server`, `workstation`, `plc`, `hmi`, `ids`, `siem`, `attacker` | a generic device |
| `io.ae3gis.type.category` | Palette category id. Built-in: `network`, `security`, `server`, `endpoint`, `ics`. A new id makes a new category (titled from the id). | a category named after the namespace |
| `io.ae3gis.type.description` | One line about the type | empty |
| `io.ae3gis.type.purdue-level` | Purdue model level, a number from 0 to 5 | none |
| `io.ae3gis.type.web-ui-port` | Port of the node's web UI | none |

Unknown `io.ae3gis.*` keys are reported as warnings (usually typos, e.g.
`io.ae3gis.type.colour`). No environment-variable label exists: bake defaults
into the image with `ENV`.

## 4. How images become types

- **A built-in type** (`io.ae3gis.type` is one AE3GIS already has, e.g. `plc`,
  `router`, `web-server`): the image joins that type as another variant. The
  type's name, role, color and default image stay as they are; `type.*` labels
  are ignored.
- **A new type**: the image labelled `io.ae3gis.default="true"` defines it
  (or, if none is, the first repo by name). That image must set
  `io.ae3gis.type.name` and `io.ae3gis.type.role`, or every image of the type is
  rejected. Other images of the type join as variants; if their `type.*` labels
  disagree with the default's, AE3GIS warns and uses the default's.
- **Two namespaces, one new type id**: the namespace added first defines the
  type; the other's images join it as variants.
- An image ref the built-in catalog already describes keeps its built-in
  description.

### The role

| Role | AE3GIS configures |
|---|---|
| `host` | one IP and a default route via the subnet's gateway |
| `router` | IP forwarding, an address per link, static routes to every subnet |
| `switch` | a Linux bridge over its ports (or only an address on `own-bridge`) |

## 5. Platforms

AE3GIS reads platforms from the tag's manifest list. Publish both
`linux/amd64` and `linux/arm64` when you can:

```sh
docker buildx build --platform linux/amd64,linux/arm64 -t <namespace>/<repo>:latest --push .
```

An image published only for another architecture still deploys: AE3GIS pulls
it for that platform (amd64 if listed) and warns that it runs emulated, which is
slower (Apple silicon runs amd64 images through Docker Desktop's emulation).

## 6. A complete example

```dockerfile
FROM ubuntu:24.04
RUN apt-get update && apt-get install -y --no-install-recommends openssh-server iproute2 \
    && rm -rf /var/lib/apt/lists/* && mkdir -p /run/sshd && echo 'root:pass' | chpasswd
CMD ["/usr/sbin/sshd", "-D"]

LABEL org.opencontainers.image.title="OpenSSH bastion" \
      org.opencontainers.image.description="Ubuntu 24.04 jump host; SSH root/pass." \
      io.ae3gis.schema="1" \
      io.ae3gis.type="bastion" \
      io.ae3gis.default="true" \
      io.ae3gis.type.name="Bastion Host" \
      io.ae3gis.type.role="host" \
      io.ae3gis.type.label="BS" \
      io.ae3gis.type.color="#7c3aed" \
      io.ae3gis.type.icon="server" \
      io.ae3gis.type.category="security" \
      io.ae3gis.type.purdue-level="3.5"
```

A variant of the built-in PLC type, on Alpine (no bash):

```dockerfile
FROM alpine:3.20
COPY plc.sh /usr/local/bin/plc.sh
CMD ["/usr/local/bin/plc.sh"]

LABEL org.opencontainers.image.title="Alpine PLC (scripts)" \
      io.ae3gis.schema="1" \
      io.ae3gis.type="plc" \
      io.ae3gis.shell="/bin/sh"
```

Then set the repo's short description to e.g. `[ae3gis] OpenSSH bastion`.

**Check the labels before pushing:**

```sh
docker inspect --format '{{json .Config.Labels}}' <namespace>/<repo>:latest
```

## 7. What AE3GIS does with your image

- Runs it with Kathará, with the image's own `CMD`/`ENTRYPOINT`.
- Writes `/ae3gis-init.sh` (addressing, routes, bridge per the role) and runs it
  at boot with bash, or `io.ae3gis.shell`; its log is
  `/var/log/ae3gis-init.log`. The image needs `ip` (iproute2 or BusyBox).
- Gives it no extra privileges: what the image needs must work unprivileged.

## 8. Syncing, rate limits and updates

- A sync lists the namespace and tags through the Hub API (free), then reads
  each marked repo's labels from the registry: one Docker Hub **pull** per image
  (anonymous: 100 per hour per IP, shared by everyone behind the same address).
- Labels are cached by digest: a later sync re-reads only images whose tag now
  points at a new digest.
- A sync stops reading while `AE3GIS_REGISTRY_PULL_RESERVE` pulls (default 10)
  are left, so deploys can still pull; the rest show as *pending* and are read
  by the next sync. Images it already knew keep their previous labels meanwhile.
- AE3GIS never syncs on its own: after pushing, press **Sync** on the registry.
  What a sync loaded survives restarts and Docker Hub outages.
- An image that opts in but breaks a rule is shown as **rejected**, with every
  reason, in the registry's details (Images → the registry → expand).

## Versioning

`io.ae3gis.schema` versions this document. A future AE3GIS that changes the
labels incompatibly reads a new schema version; images labelled `1` keep
working with the rules above.
