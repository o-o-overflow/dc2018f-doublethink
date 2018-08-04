#!/bin/bash -e

function convert_base()
{
	bc <<< "obase=$3;ibase=$2;$1"
}

mixasm -l shellcode.mixal

cat <<END | mixvm | grep -E "^[0-9]+:" | sed -e "s/.*(//" -e "s/)//" > decimals
load shellcode.mix
pmem 100-200
quit
END

BITS=$(
	for n in $(cat decimals):
	do
		printf "%030s" $(convert_base $n 10 2) | tr ' ' '0'
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
