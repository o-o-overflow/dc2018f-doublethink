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

# pad
while [ $(((${#DUMP}*3) % 8)) -ne 0 ]
do
	echo "Padding..."
	DUMP=${DUMP}0
done
echo Converting $DUMP

python -c "open('$OUT', 'wb').write(hex(int(bin(0$DUMP)[2:].rjust(3*len('$DUMP'), '0'), 2))[2:].replace('L','').decode('hex'))"
