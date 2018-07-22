#!/usr/bin/env python

import argparse
import gmpy2
import math
import sys

parser = argparse.ArgumentParser(description='Format converter.')
parser.add_argument('-c', '--chunksize', help="number of output chars per chunk", type=int, default=9999999999999999999999999999)
parser.add_argument('-p', '--padchar', help="character to pad with (for base 256)", type=str, default=" ")
parser.add_argument('base', type=int)
parser.add_argument('file', help="file", nargs='?', type=argparse.FileType('r'), default=sys.stdin)
args = parser.parse_args()

strbin = bin(int(args.file.read().encode('hex'), 16))[2:]
strbin = "0"*((-len(strbin))%8) + strbin # pad the front
basebits = int(math.log(args.base, 2))
assert int(basebits) == basebits, "Base must be a power of 2."

if args.base <= 32:
	chunkbits = basebits * args.chunksize
	to_pad = (-len(strbin)) % chunkbits
	strbin += '0' * to_pad
	strbase = gmpy2.digits(int(strbin, 2), args.base)
elif args.base == 256:
	strbase = hex(int(strbin, 2))[2:].replace('L','').decode('hex')
	to_pad = (-len(strbin)) % args.chunksize
	strbase += args.padchar * to_pad
else:
	raise Exception("unsupported base")

print ' '.join(strbase[i:i+args.chunksize] for i in range(0, len(strbase), args.chunksize))
