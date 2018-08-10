#!/bin/bash -e

echo
echo "[###] amd64..."
(cd interaction/platforms/amd64 && ./dump.sh)
service/scripts/run_emu.sh amd64 OOO1234567890 interaction/platforms/amd64/shellcode

echo
echo "[###] arm64..."
(cd interaction/platforms/arm64 && ./dump.sh)
service/scripts/run_emu.sh arm64 OOO1234567890 interaction/platforms/arm64/shellcode

echo
echo "[###] mipsel..."
(cd interaction/platforms/mipsel && ./dump.sh)
service/scripts/run_emu.sh mipsel OOO1234567890 interaction/platforms/mipsel/shellcode

echo
echo "[###] PDP-1..."
(cd interaction/platforms/pdp-1 && ./dump.sh)
service/scripts/run_emu.sh pdp-1 OOO1234567890 interaction/platforms/pdp-1/shellcode

echo
echo "[###] PDP-8..."
(cd interaction/platforms/pdp-8 && ./dump.sh)
service/scripts/run_emu.sh pdp-8 OOO1234567890 interaction/platforms/pdp-8/shellcode

echo
echo "[###] PDP-10..."
(cd interaction/platforms/pdp-8 && ./dump.sh)
service/scripts/run_emu.sh pdp-10 OOO1234567890 interaction/platforms/pdp-10/shellcode

echo
echo "[###] IBM-1401..."
(cd interaction/platforms/ibm-1401 && ./dump.sh)
service/scripts/run_emu.sh ibm-1401 OOO1234567890 interaction/platforms/ibm-1401/shellcode

echo
echo "[###] DG Nova..."
(cd interaction/platforms/nova && ./dump.sh)
service/scripts/run_emu.sh nova OOO1234567890 interaction/platforms/nova/shellcode

echo
echo "[###] LGP-30..."
(cd interaction/platforms/lgp-30 && ./dump.sh)
service/scripts/run_emu.sh lgp-30 OOO1234567890 interaction/platforms/lgp-30/shellcode

echo
echo "[###] MIX..."
(cd interaction/platforms/mix && ./dump.sh)
service/scripts/run_emu.sh mix OOO1234567890 interaction/platforms/mix/shellcode

echo
echo "[###] Hexagon..."
#(cd interaction/platforms/hexagon && ./dump.sh)
service/scripts/run_emu.sh hexagon OOO1234567890 interaction/platforms/hexagon/shellcode

echo
echo "[###] MMIX..."
(cd interaction/platforms/mmix && ./dump.sh)
service/scripts/run_emu.sh mmix OOO1234567890 interaction/platforms/mmix/shellcode

echo
echo "[###] risc-v..."
(cd interaction/platforms/risc-v && ./dump.sh)
service/scripts/run_emu.sh risc-v OOO1234567890 interaction/platforms/risc-v/shellcode

echo
echo "[###] cLEMENCy..."
(cd interaction/platforms/clemency && ./dump.sh)
service/scripts/run_emu.sh clemency OOO1234567890 interaction/platforms/clemency/shellcode

echo "[###] SUCCESS!"
