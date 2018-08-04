#!/bin/bash -e

function convert_base()
{
	bc <<< "obase=$3;ibase=$2;$1"
}

{
	IFS=$'\n'
	addr=64
	for line in $(cat shellcode.asm)
	do
		printf "d -mt %s %s\n" $(convert_base $addr 10 8) $line
		addr=$(($addr+1))
	done

	for i in $(seq 64 $addr)
	do
		printf "e %s\n" $(convert_base $i 10 8)
	done

	echo exit
} > commands.in

BITS=$(
	for n in $(pdp10 commands.in | grep -E "^[0-9]+:" | sed -e "s/^[0-9]\+:\s\+//")
	do
		printf "%036s" $(bc <<< "obase=2;ibase=8;$n") | tr ' ' '0'
	done
)
# pad
while [ $((${#BITS} % 8)) -ne 0 ]
do
        echo "Padding..."
        BITS=${BITS}0
done
echo Bits: $BITS

HEX=$(bc <<< "obase=16;ibase=2;$BITS" | tr -d '\\\n ')
# pad
echo ${#HEX} ${#BITS}
while [ $((${#HEX} * 4)) -ne ${#BITS} ]
do
        echo "Padding..."
        HEX=0${HEX}
done
echo Hex: $HEX

echo $HEX | xxd -r -p > shellcode
