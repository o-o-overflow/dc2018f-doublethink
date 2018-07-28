#!/usr/bin/env python

import argparse
#import gmpy2
#import math
#import sys

def chunk_str(s, chunksize):
	return [ s[i:i+chunksize] for i in range(0, len(s), chunksize) ]

def hex2int(s):
	return int(s.encode('hex'), 16)
def bin2hex(s):
	return hex(int(s,2))[2:].strip('L')
def bin2oct(s):
	return oct(int(s,2))[1:].strip('L')

class Emu(object):
	def __init__(self, flag, shellcode):
		self.flag_file = flag
		self.flag = open(self.flag_file).read().strip()
		self.flag_bits = bin(int(self.flag.encode('hex'), 16))[2:].rjust(len(self.flag)*8, '0')
		self.shellcode_file = shellcode
		self.shellcode = open(self.shellcode_file).read()
		self.shellcode_bits = bin(int(self.shellcode.encode('hex'), 16))[2:].rjust(len(self.shellcode)*8, '0')

	def _emit(self, *s): #pylint:disable=no-self-use
		print ' '.join(str(e) for e in s)

	def emit_flag(self):
		raise NotImplementedError()

	def emit_shellcode(self):
		raise NotImplementedError()

	def start(self):
		self._emit('run 100')

	def quit(self):
		self._emit('exit')

#pylint:disable=abstract-method
class EmuPDP1(Emu):
	def emit_flag(self):
		for i, fw in enumerate(chunk_str(self.flag, 3)):
			self._emit('d', oct(i), '''"%s"''' % fw.ljust(3))

	def emit_shellcode(self):
		for i, sw in enumerate(chunk_str(self.shellcode_bits, 18)):
			ow = oct(int(sw,2))[1:].replace('L','').rjust(6, '0')
			self._emit('d', oct(64+i), ow)

class EmuPDP8(Emu):
	def emit_flag(self):
		for i, fw in enumerate(chunk_str(self.flag, 1), start=01337):
			self._emit('d', oct(i), """'%s""" % fw)

	def emit_shellcode(self):
		for i, sw in enumerate(chunk_str(self.shellcode_bits, 12), start=64):
			ow = oct(int(sw,2))[1:].replace('L','').rjust(4, '0')
			self._emit('d', oct(i), ow)

class EmuIBM1401(Emu):
	def start(self):
		self._emit('att lpt /dev/stdout')
		self._emit('run 1')

	def emit_flag(self):
		for i, fw in enumerate(chunk_str(self.flag, 1), start=900):
			self._emit('d', i, """'%s""" % fw)

	def emit_shellcode(self):
		for i, sw in enumerate(chunk_str(self.shellcode_bits, 7), start=0):
			ow = oct(int(sw,2))[1:].replace('L','').rjust(3, '0')
			self._emit('d', i, ow)

class EmuNova(Emu):
	def emit_flag(self):
		for i, fw in enumerate(chunk_str(self.flag, 2), start=01337):
			self._emit('d', oct(i), oct(int(fw.ljust(2).encode('hex'),16)))

	def emit_shellcode(self):
		for i, sw in enumerate(chunk_str(self.shellcode_bits, 16), start=0100):
			ow = oct(int(sw,2))[1:].replace('L','').rjust(6, '0')
			self._emit('d', oct(i), ow)

class EmuLGP30(Emu):
	@staticmethod
	def _make_addr(i):
		return "%02d%02d" % (i/64, i%64)

	LETTER_BITS = {
    	'0': '000010', '1': '000110', '2': '001010', '3': '001110', '4': '010010', '5': '010110', '6': '011010', '7': '011110', '8': '100010', '9': '100110',
    	'A': '111001', 'B': '000101', 'C': '110101', 'D': '010101', 'E': '100101',
    	'F': '101010', 'G': '101110', 'H': '110001', 'I': '010001', 'J': '110010',
    	'K': '110110', 'M': '011101', 'N': '011001', 'O': '100011', 'P': '100001', # L is fucking uppercase 1...
    	'Q': '111010', 'R': '001101', 'S': '111101', 'T': '101101', 'U': '101001',
    	'V': '011111', 'W': '111110', 'X': '100111', 'Y': '001001', 'Z': '000001',
	}
	LETTERS = { letter:bin2hex(bits).zfill(2)+'00' for letter,bits in LETTER_BITS.items() }

	def emit_flag(self):
		for i, c in enumerate(chunk_str(self.flag, 1), start=13*64+37):
			self._emit('d', self._make_addr(i), EmuLGP30.LETTERS[c])

	def emit_shellcode(self):
		for i, sw in enumerate(chunk_str(self.shellcode_bits, 31), start=0100):
			if len(sw) < 31:
				continue
			self._emit('d', self._make_addr(i), bin2hex(sw+'0').zfill(8))

platforms = {
	'pdp-1': EmuPDP1,
	'pdp-8': EmuPDP8,
	'ibm-1401': EmuIBM1401,
	'nova': EmuNova,
	'lgp-30': EmuLGP30,
}

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Format converter.')
	parser.add_argument('machine', help="the machine type")
	parser.add_argument('flag', help="the flag file")
	parser.add_argument('shellcode', help="the shellcode file")
	args = parser.parse_args()

	e = platforms[args.machine](args.flag, args.shellcode)
	e.emit_flag()
	e.emit_shellcode()
	e.start()
	e.quit()
