#!/usr/bin/env bash
# Runs on every boot; idempotent.
set -euxo pipefail

if [ ! -f /var/lib/scriptcut-bootstrapped ]; then
  fallocate -l 2G /swapfile && chmod 600 /swapfile && mkswap /swapfile && swapon /swapfile
  echo '/swapfile none swap sw 0 0' >> /etc/fstab

  apt-get update
  apt-get install -y ca-certificates curl
  curl -fsSL https://get.docker.com | sh
  systemctl enable --now docker
  mkdir -p /opt/scriptcut
  touch /var/lib/scriptcut-bootstrapped
fi
