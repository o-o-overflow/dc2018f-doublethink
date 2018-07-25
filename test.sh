#!/bin/bash -e

echo "[###] PDP-1..."
service/scripts/run.sh pdp-1 OOO1234567890 sanity-check/pdp-1/shellcode

echo "[###] SUCCESS!"
