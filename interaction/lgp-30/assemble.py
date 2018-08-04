#!/usr/bin/env python

letters = {
    '0': '000010', '1': '000011', '2': '001010', '3': '001110', '4': '010010', '5': '010110', '6': '011010', '7': '011110', '8': '100010', '9': '100110',
    'A': '111001', 'B': '000101', 'C': '110101', 'D': '010101', 'E': '100101',
	'F': '101010', 'G': '101110', 'H': '110001', 'I': '010001', 'J': '110010',
	'K': '110110', 'M': '011101', 'N': '011001', 'O': '100011', 'P': '100001', # L is fucking uppercase 1...
	'Q': '111010', 'R': '001101', 'S': '111101', 'T': '101101', 'U': '101001',
	'V': '011111', 'W': '111110', 'X': '100111', 'Y': '001001', 'Z': '000001',
}

opcodes = {
	'B': '0001', # mn Bring accumulator from memory cell mn "Bring"
	'H': '1100', # mn Store accumulator in mn and hold "Hold"
	'C': '1101', # mn Store accumulator in mn and clear "Clear"
	'A': '1110', # mn Add "Add"
	'S': '1111', # mn Subtract "Subtract"
	'M': '0111', # mn Multipliy, keep top half "Multiply"
	'N': '0110', # mn Multipliy, keep bottom half
	'D': '0101', # mn Divide "Divide"
	'E': '1001', # mn Logical product (AND) "Extract"
	'U': '1010', # mn Unconditional jump to mn "Unconditional jump"
	'T': '1011', # mn Jump to mn if accumulator is negative "Test and jump"
	'Y': '0010', # mn Replace address part
	'R': '0011', # mn Store return address "Return"
	'I': '0100', # Input "Input"
	'P': '1000', # m Print symbol denoted by m "Print"
	'Z': '0000', # m Halt if the breakpoint switch associated with m is not depre
}

def assemble_bits(s):
	opcode = s.split()[0]
	args = s.split()[1:]
	argbits = '0'*12 if not args else bin(int(args[0], 0))[2:]
	instbits = '0'*12 + opcodes[opcode] + '00' + argbits.zfill(12) + '0'
	assert len(instbits) == 31
	return instbits

def assemble_simh(start, args, more=()):
	i = 0
	for i,n in enumerate(args, start=start):
		asmbits = assemble_bits(n)
		asmint = int(asmbits+'0', 2)
		asmhex = hex(asmint)[2:].zfill(8)
		yield "echo INSTRUCTION AT %d: %s (%s)" % (i,n,asmhex)
		yield "d %s %s" % (i,asmhex)

	# test it
	yield "e -m %s-%s" % (start, i-1)
	yield "d c %s" % i
	yield "step 1"
	for i,m in enumerate(more, start=start+len(args)):
		yield 'd %s %s' % (i, m)

def assemble_bytes(start, args, more=()): #pylint:disable=unused-argument
	bits = ''.join(assemble_bits(i) for i in args)
	bits += ''.join(bin(int(n.zfill(8), 16))[2:].zfill(31) for n in more)
	assert len(bits) % 31 == 0
	bits += '0'*((-len(bits))%8)
	assert len(bits) % 8 == 0
	h = hex(int(bits,2))[2:].replace('L','').zfill(len(bits)/4)
	return h.decode('hex')

if __name__ == '__main__':
	for _i in reversed(range(1, 2**12)):
		print '\n'.join(assemble_simh(100, [
			"P %s" % bin(_i),
			"P %s" % bin(_i),
			"P %s" % bin(_i),
			"P %s" % bin(_i),
			"P %s" % bin(_i),
			"P %s" % bin(_i),
			#"A 0",
			#"A 0",
			#"A 0",
			#"A 0",
			#"A 0",
			#"A 0",
		]))
	#for c,n in sorted(letters.items()):
	#	print "echo LETTER:",c
	#	print '\n'.join(assemble_simh(100, ["P 0b%s" % (n+n)]))
	#shellcode = [ ]
	#for c in letters.values():
	#	shellcode += [ 'P 0b'+c.ljust(12, '0') ]
	#print '\n'.join(assemble_simh(100, shellcode))
	#print "run 100"
	print "exit"
	#open('shellcode', 'w').write(assemble_bytes(100, shellcode))
