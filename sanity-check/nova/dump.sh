#!/bin/bash

[ -f numbers ] || ( echo 'obase=8'; echo {1..65535} | tr ' ' '\n' ) | bc > numbers
[ -f disassemble ] || ( cat numbers | bc | sed -e "s/.*/echo &\nd 0 &\ne -m 0/"; echo exit ) > disassemble
[ -f disassembled ] || dgnova -q disassemble > disassembled
./assemble.py
