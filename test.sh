#!/bin/bash -e

echo
echo "[###] PDP-1..."
service/scripts/run.sh pdp-1 OOO1234567890 sanity-check/pdp-1/shellcode

echo
echo "[###] PDP-8..."
service/scripts/run.sh pdp-8 OOO1234567890 sanity-check/pdp-8/shellcode

echo "[###] SUCCESS!"
