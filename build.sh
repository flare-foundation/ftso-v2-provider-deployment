#!/usr/bin/env bash

set -eu

source <(grep -v '^#' "./.env" | sed -E 's|^(.+)=(.*)$|: ${\1=\2}; export \1|g')

# c chain indexer
docker build \
    -t "ftso-v2-deployment/flare-system-c-indexer" \
    "./build/flare-system-c-chain-indexer"

# flare system client
docker build \
    -t "ftso-v2-deployment/flare-system-client" \
    "./build/flare-system-client"

# ftso scaling
docker build \
    -t "ftso-v2-deployment/ftso-scaling" \
    "./build/ftso-scaling"

