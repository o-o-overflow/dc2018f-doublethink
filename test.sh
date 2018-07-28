#!/bin/bash -ex

echo
echo "[###] PDP-1..."
(cd sanity-check/pdp-1 && ./dump.sh)
service/scripts/run.sh pdp-1 OOO1234567890 sanity-check/pdp-1/shellcode

echo
echo "[###] PDP-8..."
(cd sanity-check/pdp-8 && ./dump.sh)
service/scripts/run.sh pdp-8 OOO1234567890 sanity-check/pdp-8/shellcode

echo
echo "[###] PDP-10..."
(cd sanity-check/pdp-8 && ./dump.sh)
service/scripts/run.sh pdp-10 OOO1234567890 sanity-check/pdp-10/shellcode

echo
echo "[###] IBM-1401..."
(cd sanity-check/ibm-1401 && ./dump.sh)
service/scripts/run.sh ibm-1401 OOO1234567890 sanity-check/ibm-1401/shellcode

echo
echo "[###] DG Nova..."
(cd sanity-check/nova && ./dump.sh)
service/scripts/run.sh nova OOO1234567890 sanity-check/nova/shellcode

echo
echo "[###] LGP-30..."
(cd sanity-check/lgp-30 && ./dump.sh)
service/scripts/run.sh lgp-30 OOO1234567890 sanity-check/lgp-30/shellcode

echo
echo "[###] MIX..."
(cd sanity-check/mix && ./dump.sh)
service/scripts/run.sh mix OOO1234567890 sanity-check/mix/shellcode

echo "[###] SUCCESS!"
