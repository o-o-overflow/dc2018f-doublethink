#!/bin/bash -e

if [ ! -f riscv-tools ]
then
	echo "riscv tools not installed."
	exit
fi

riscv-tools/bin/riscv64-unknown-elf-as shellcode.s -o shellcode.o
riscv-tools/bin/riscv64-unknown-elf-objcopy --dump-section .text=shellcode shellcode.o
