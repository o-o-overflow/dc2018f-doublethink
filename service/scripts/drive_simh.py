#!/usr/bin/env python

import argparse
#import gmpy2
#import math
#import sys

def chunk_str(s, chunksize):
	return [ s[i:i+chunksize] for i in range(0, len(s), chunksize) ]

def s2i(s):
	return int(s.encode('hex'), 16)

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
			self._emit('d', oct(i), '''"%s"''' % fw)

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

platforms = {
	'pdp-1': EmuPDP1,
	'pdp-8': EmuPDP8,
	'ibm-1401': EmuIBM1401,
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
