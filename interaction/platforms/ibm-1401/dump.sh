#!/bin/bash -e

CARD=shellcode.card
OUT=shellcode

(
	echo att cdr $CARD
	echo att lpr /dev/null
	echo boot cdr
	echo e 0-100
	echo exit
) > commands.in

DUMP=$(
	for n in $(i1401 commands.in | grep $':\t' | sed -e "s/.*:\t//")
	do
		printf "%7s" $(bc <<< "obase=2;ibase=8;$n") | tr ' ' '0'
	done
)
echo $DUMP

# pad
while [ $((${#DUMP} % 8)) -ne 0 ]
do
	echo "Padding..."
	DUMP=${DUMP}0
done
echo Converting $DUMP

python -c "open('$OUT', 'wb').write(hex(0b$DUMP)[2:].replace('L','').decode('hex'))"
