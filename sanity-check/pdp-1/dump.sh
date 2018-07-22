#!/bin/bash -e

ASM=$1.mac
BIN=$1.rim
OUT=$2
ADDR=64
LEN=22

macro1 $ASM

(
	echo att ptr $BIN
	echo break $ADDR
	echo boot ptr
	for i in $(seq $ADDR $(($ADDR+$LEN)))
	do
		printf "e %o\n" $i
	done
	echo exit
) > commands.in

DUMP=$(pdp1 commands.in | grep $':\t' | sed -e "s/.*:\t//" | tr -d '\n')

python -c "open('$OUT', 'wb').write(hex(0$DUMP)[2:].replace('L','').decode('hex'))"
