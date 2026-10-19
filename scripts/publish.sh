#!/usr/bin/env bash
# Publish the images listed in images.tsv to Docker Hub for AE3GIS (see README.md).
#
#   scripts/publish.sh [folder...]           build, push <ns>/<folder>:<version> and :latest
#   scripts/publish.sh describe [folder...]  set each repo's "[ae3gis] <title>" description
#
# No folder means every row of images.tsv.
#
# Environment:
#   HUB_NAMESPACE       Docker Hub namespace (default: tollan)
#   DOCKERHUB_USERNAME  account for "describe" (default: the namespace)
#   DOCKERHUB_TOKEN     personal access token for "describe" (Read, Write, Delete);
#                       prompted for if unset
set -euo pipefail

cd "$(dirname "$0")/.."

NAMESPACE=${HUB_NAMESPACE:-tollan}
HUB=https://hub.docker.com

die() { echo "error: $*" >&2; exit 1; }

# Prints "folder version platforms" for each requested folder (all rows if none)
rows() {
  local want=" $* "
  local found=0 folder version platforms
  while read -r folder version platforms; do
    case "$folder" in ''|'#'*) continue ;; esac
    if [ $# -eq 0 ] || [[ "$want" == *" $folder "* ]]; then
      echo "$folder $version $platforms"
      found=$((found + 1))
    fi
  done < images.tsv
  [ $# -eq 0 ] || [ "$found" -eq $# ] || die "not every folder in '$*' is listed in images.tsv"
}

# The pushed image's labels, as JSON (from the first platform's config)
labels() {
  docker buildx imagetools inspect "$1" --format '{{json .Image}}' |
    jq -c 'if has("config") then .config.Labels else (to_entries[0].value.config.Labels) end'
}

publish() {
  local folder=$1 version=$2 platforms=$3
  local repo ref status
  repo=$(basename "$folder")
  ref="$NAMESPACE/$repo"

  status=$(curl -s -o /dev/null -w '%{http_code}' \
    "$HUB/v2/namespaces/$NAMESPACE/repositories/$repo/tags/$version")
  [ "$status" = 404 ] || die "$ref:$version already exists on Docker Hub (HTTP $status): bump its version in images.tsv"

  echo "==> $ref:$version ($platforms)"
  docker buildx build --platform "$platforms" -f "$folder/dockerfile" \
    -t "$ref:$version" -t "$ref:latest" --push "$folder"

  local got
  got=$(labels "$ref:$version")
  jq -e '.["io.ae3gis.schema"] == "1" and (.["io.ae3gis.type"] // "") != ""' <<<"$got" >/dev/null ||
    die "$ref:$version is missing io.ae3gis.schema=1 or io.ae3gis.type: $got"
  echo "    pushed $ref:$version and :latest, type $(jq -r '.["io.ae3gis.type"]' <<<"$got")"
}

describe() {
  local user=${DOCKERHUB_USERNAME:-$NAMESPACE}
  local secret=${DOCKERHUB_TOKEN:-}
  if [ -z "$secret" ]; then
    read -rsp "Docker Hub access token for $user: " secret
    echo
  fi
  local jwt
  jwt=$(jq -n --arg u "$user" --arg s "$secret" '{identifier: $u, secret: $s}' |
    curl -sf -X POST "$HUB/v2/auth/token" -H 'Content-Type: application/json' -d @- |
    jq -r '.access_token // empty') || true
  [ -n "$jwt" ] || die "Docker Hub rejected the token for $user"

  local folder version platforms repo title body status readme scheme
  while read -r folder version platforms; do
    repo=$(basename "$folder")
    title=$(labels "$NAMESPACE/$repo:$version" | jq -r '.["org.opencontainers.image.title"] // empty')
    [ -n "$title" ] || die "$NAMESPACE/$repo:$version has no org.opencontainers.image.title (push it first)"
    readme=$(ls "$folder"/README.md "$folder"/readme.md 2>/dev/null | head -1 || true)
    body=$(jq -n --arg d "[ae3gis] $title" --rawfile f "${readme:-/dev/null}" \
      '{description: $d[0:100], full_description: $f[0:25000]}')
    # Bearer is the current scheme; older Hub endpoints answered to "JWT"
    for scheme in Bearer JWT; do
      status=$(curl -s -o /dev/null -w '%{http_code}' -X PATCH \
        "$HUB/v2/repositories/$NAMESPACE/$repo/" \
        -H "Authorization: $scheme $jwt" -H 'Content-Type: application/json' -d "$body")
      [ "$status" = 401 ] || break
    done
    [ "$status" = 200 ] || die "could not update $NAMESPACE/$repo (HTTP $status)"
    echo "    $NAMESPACE/$repo: [ae3gis] $title"
  done <<<"$1"
}

command -v jq >/dev/null || die "jq is required"

mode=publish
if [ "${1:-}" = describe ]; then
  mode=describe
  shift
fi
list=$(rows "$@")

if [ "$mode" = describe ]; then
  describe "$list"
else
  while read -r folder version platforms; do
    publish "$folder" "$version" "$platforms"
  done <<<"$list"
fi
