#!/bin/bash -e

{
	IFS=$'\n'
	addr=64
	for line in $(cat shellcode.asm)
	do
		printf "d -mt %02d%02d %s\n" $(($addr/64)) $(($addr%64)) $line
		addr=$(($addr+1))
	done

	for i in $(seq 64 $addr)
	do
		printf "e %02d%02d\n" $(($i/64)) $(($i%64))
	done

	echo exit
} > commands.in

BITS=$(
	for n in $(lgp commands.in | grep -E "^[0-9]+:" | sed -e "s/^[0-9]\+:\s\+//")
	do
		printf "%032s" $(bc <<< "obase=2;ibase=16;$n") | tr ' ' '0'  | head -c 31
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
