#!/bin/bash
# SSL Certificate Fix for macOS Python
export SSL_CERT_FILE=$(python3 -m certifi)
echo "✅ SSL certificates configured"
echo "Certificate file: $SSL_CERT_FILE"
