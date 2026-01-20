#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

[ ! -f "$SCRIPT_DIR/config/kubeconfig" ] && echo "ERROR: kubeconfig not found at $SCRIPT_DIR/config/kubeconfig" && exit 1

docker run --rm --net=host --platform linux/amd64 \
    -v "$SCRIPT_DIR/config/kubeconfig:/home/krkn/.kube/config:Z" \
    -v "$SCRIPT_DIR/config:/home/krkn/config:Z" \
    quay.io/krkn-chaos/krkn:latest \
    --config=/home/krkn/config/config.yaml
