#!/bin/bash
set -e

CERT_DIR="./certs"
mkdir -p "$CERT_DIR"

echo "Generating self-signed certificate..."

openssl req -x509 \
  -newkey rsa:2048 \
  -keyout "$CERT_DIR/key.pem" \
  -out "$CERT_DIR/cert.pem" \
  -days 365 \
  -nodes \
  -subj "/C=US/ST=Florida/L=Miami/O=Demo/CN=localhost"

echo "Done! Certificate files created in $CERT_DIR/"
