#!/bin/bash -e

../../service/platforms/mmix/mmixal -l shellcode.lst shellcode.mms
cat <<END | ../../service/platforms/mmix/mmix -i shellcode.mmo | grep M8 | sed -e "s/.*#//" | parallel "printf '%016x' 0x{}" | xxd -r -p > shellcode
M200#
M208#
M210#
M218#
M220#
M228#
M230#
M238#
M240#
M248#
M250#
M258#
M260#
M268#
M270#
M278#
M280#
M288#
quit
END
