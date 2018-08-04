#!/usr/bin/env python

# Blatantly stolen from Shellphish's toolset from DEFCON 2017

"""
Celemency assembler supporting labels.

A sample program computing 1+2+...+100:

    ldt r1, [r0 + data, 1]
next:
    adi r2, r2, 1
    ad r3, r3, r2
    cm r2, r1
    bl next
    ht
data:
    .dt 100
"""
import logging
import re
import sys
import bitstring
from functools import partial

logger = logging.getLogger("assemble")
first_pass = True
pc = 0
labels = dict()

def _encode_num(n, size):
    x = bin(int(n, 0) & ((1 << size) - 1))[2:].zfill(size)
    return x

def _encode_reg_count(n, size):
    return _encode_num(str(int(n, 0) - 1), size)

def _encode_location(label_or_location):
    if first_pass:
        return "0" * 27
    if label_or_location in labels:
        location = str(labels[label_or_location])
    else:
        location = label_or_location
    return _encode_num(location, 27)

def _encode_offset(label_or_offset, size=27):
    if first_pass:
        return "0" * size
    global pc
    if label_or_offset in labels:
        location = labels[label_or_offset]
        offset = str(location - pc)
    else:
        offset = label_or_offset
    return _encode_num(offset, size)

def _encode_reg(reg):
    x = bin(int(reg.lower().replace('st', 'r29').replace('sp', 'r29').replace('ra', 'r30').replace('pc', 'r31').replace('r', '')))[2:].zfill(5)
    if len(x) > 5:
        raise ValueError("encoded number too large")
    return x

def encode_me(bits):
    if len(bits) == 0:
        return ''
    elif len(bits) == 18:
        return bits[9:18] + bits[0:9]
    elif len(bits) == 27:
        return bits[9:18] + bits[0:9] + bits[18:27]
    elif len(bits) == 36:
        return bits[9:18] + bits[0:9] + bits[18:27] + bits[27:36]
    elif len(bits) == 54:
        return bits[9:18] + bits[0:9] + bits[18:27] + bits[36:45] + bits[27:36] + bits[45:54]
    else:
        raise ValueError('unsupported bit length')

def to_bin(s):
    return bitstring.BitArray(bin=s+'0'*(8-len(s)%8)).bytes

#
# ADD HANDLERS BELOW HERE
#

# A

def assemble_ad(rA, rB, rC, *args):
    "Yan"
    return "0000000" + _encode_reg(rA) + _encode_reg(rB) + _encode_reg(rC) + "0000" + ("1" if len(args) else "0")

def assemble_adc(rA, rB, rC, *args):
    "Yan"
    return "0100000" + _encode_reg(rA) + _encode_reg(rB) + _encode_reg(rC) + "0000" + ("1" if len(args) else "0")

def assemble_adci(rA, rB, imm, *args):
    "Yan"
    return "0100000" + _encode_reg(rA) + _encode_reg(rB) + _encode_num(imm, 7) + "01" + ("1" if len(args) else "0")

def assemble_adcim(rA, rB, imm, *args):
    "Yan"
    return "0100010" + _encode_reg(rA) + _encode_reg(rB) + _encode_num(imm, 7) + "01" + ("1" if len(args) else "0")

def assemble_adcm(rA, rB, rC, *args):
    "Yan"
    return "0100010" + _encode_reg(rA) + _encode_reg(rB) + _encode_reg(rC) + "0000" + ("1" if len(args) else "0")

def assemble_adf(rA, rB, rC, *args):
    "Yan"
    return "0000001" + _encode_reg(rA) + _encode_reg(rB) + _encode_reg(rC) + "0000" + ("1" if len(args) else "0")

def assemble_adfm(rA, rB, rC, *args):
    "Yan"
    return "0000011" + _encode_reg(rA) + _encode_reg(rB) + _encode_reg(rC) + "0000" + ("1" if len(args) else "0")

def assemble_adi(rA, rB, imm, *args):
    "Yan"
    return "0000000" + _encode_reg(rA) + _encode_reg(rB) + _encode_num(imm, 7) + "01" + ("1" if len(args) else "0")

def assemble_adim(rA, rB, imm, *args):
    "Yan"
    return "0000010" + _encode_reg(rA) + _encode_reg(rB) + _encode_num(imm, 7) + "01" + ("1" if len(args) else "0")

def assemble_adm(rA, rB, rC, *args):
    "Yan"
    return "0000010" + _encode_reg(rA) + _encode_reg(rB) + _encode_reg(rC) + "0000" + ("1" if len(args) else "0")

def assemble_an(rA, rB, rC, *args):
    "Yan"
    return "0010100" + _encode_reg(rA) + _encode_reg(rB) + _encode_reg(rC) + "0000" + ("1" if len(args) else "0")

def assemble_ani(rA, rB, imm, *args):
    "Yan"
    return "0010100" + _encode_reg(rA) + _encode_reg(rB) + _encode_num(imm, 7) + "01" + ("1" if len(args) else "0")

def assemble_anm(rA, rB, rC, *args):
    "Yan"
    return "0010110" + _encode_reg(rA) + _encode_reg(rB) + _encode_reg(rC) + "0000" + ("1" if len(args) else "0")
# B

def assemble_b(offset):
    return "110000" + "1111" + _encode_offset(offset, 17)

def assemble_bn(offset):
    return "110000" + "0000" + _encode_offset(offset, 17)

def assemble_be(offset):
    return "110000" + "0001" + _encode_offset(offset, 17)

def assemble_bl(offset):
    return "110000" + "0010" + _encode_offset(offset, 17)

def assemble_ble(offset):
    return "110000" + "0011" + _encode_offset(offset, 17)

def assemble_bg(offset):
    return "110000" + "0100" + _encode_offset(offset, 17)

def assemble_bge(offset):
    return "110000" + "0101" + _encode_offset(offset, 17)

def assemble_bno(offset):
    return "110000" + "0110" + _encode_offset(offset, 17)

def assemble_bo(offset):
    return "110000" + "0111" + _encode_offset(offset, 17)

def assemble_bns(offset):
    return "110000" + "1000" + _encode_offset(offset, 17)

def assemble_bs(offset):
    return "110000" + "1001" + _encode_offset(offset, 17)

def assemble_bsl(offset):
    return "110000" + "1010" + _encode_offset(offset, 17)

def assemble_bsle(offset):
    return "110000" + "1011" + _encode_offset(offset, 17)

def assemble_bsg(offset):
    return "110000" + "1100" + _encode_offset(offset, 17)

def assemble_bsge(offset):
    return "110000" + "1101" + _encode_offset(offset, 17)

def assemble_bf(rA, rB, *args):
    return "101001100" + _encode_reg(rA) + _encode_reg(rB) + "1000000" + ("1" if len(args) else "0")

def assemble_bfm(rA, rB, *args):
    return "101001100" + _encode_reg(rA) + _encode_reg(rB) + "1000000" + ("1" if len(args) else "0")

def assemble_br(rA):
    return "110000" + "1111" + _encode_reg(rA) + "000"

def assemble_brn(rA):
    return "110000" + "0000" + _encode_reg(rA) + "000"

def assemble_bre(rA):
    return "110000" + "0001" + _encode_reg(rA) + "000"

def assemble_brl(rA):
    return "110000" + "0010" + _encode_reg(rA) + "000"

def assemble_brle(rA):
    return "110000" + "0011" + _encode_reg(rA) + "000"

def assemble_brg(rA):
    return "110000" + "0100" + _encode_reg(rA) + "000"

def assemble_brge(rA):
    return "110000" + "0101" + _encode_reg(rA) + "000"

def assemble_brno(rA):
    return "110000" + "0110" + _encode_reg(rA) + "000"

def assemble_bro(rA):
    return "110000" + "0111" + _encode_reg(rA) + "000"

def assemble_brns(rA):
    return "110000" + "1000" + _encode_reg(rA) + "000"

def assemble_brs(rA):
    return "110000" + "1001" + _encode_reg(rA) + "000"

def assemble_brsl(rA):
    return "110000" + "1010" + _encode_reg(rA) + "000"

def assemble_brsle(rA):
    return "110000" + "1011" + _encode_reg(rA) + "000"

def assemble_brsg(rA):
    return "110000" + "1100" + _encode_reg(rA) + "000"

def assemble_brsge(rA):
    return "110000" + "1101" + _encode_reg(rA) + "000"

def assemble_bra(location):
    return "111000100" + _encode_location(location)

def assemble_brr(offset):
    return "111000000" + _encode_offset(offset)
# C

# zanardi
# C: Call Conditional
def assemble_cn(offset, *args):
    return "110101" + "0000" + _encode_offset(offset, 17)

def assemble_ce(offset, *args):
    return "110101" + "0001" + _encode_offset(offset, 17)

def assemble_cl(offset, *args):
    return "110101" + "0010" + _encode_offset(offset, 17)

def assemble_cle(offset, *args):
    return "110101" + "0011" + _encode_offset(offset, 17)

def assemble_cg(offset, *args):
    return "110101" + "0100" + _encode_offset(offset, 17)

def assemble_cge(offset, *args):
    return "110101" + "0101" + _encode_offset(offset, 17)

def assemble_cno(offset, *args):
    return "110101" + "0110" + _encode_offset(offset, 17)

def assemble_co(offset, *args):
    return "110101" + "0111" + _encode_offset(offset, 17)

def assemble_cns(offset, *args):
    return "110101" + "1000" + _encode_offset(offset, 17)

def assemble_cs(offset, *args):
    return "110101" + "1001" + _encode_offset(offset, 17)

def assemble_csl(offset, *args):
    return "110101" + "1010" + _encode_offset(offset, 17)

def assemble_csle(offset, *args):
    return "110101" + "1011" + _encode_offset(offset, 17)

def assemble_csg(offset, *args):
    return "110101" + "1100" + _encode_offset(offset, 17)

def assemble_csge(offset, *args):
    return "110101" + "1101" + _encode_offset(offset, 17)

def assemble_c(offset, *args):
    return "110101" + "1111" + _encode_offset(offset, 17)

# CAA: Call Absolute
def assemble_caa(location, *args):
    return "111001100" + _encode_location(location)

# CAR: Call Relative
def assemble_car(offset, *args):
    return "111001000" + _encode_offset(offset)

# CM: Compare
def assemble_cm(rA, rB, *args):
    return "10111000" + _encode_reg(rA) + _encode_reg(rB)

# CMF: Compare Floating Point
def assemble_cmf(rA, rB, *args):
    return "10111010" + _encode_reg(rA) + _encode_reg(rB)

# CMFM: Compare Floating Point Multi Reg
def assemble_cmfm(rA, rB, *args):
    return "10111110" + _encode_reg(rA) + _encode_reg(rB)

# CMI: Compare Immediate
def assemble_cmi(rA, imm, *args):
    return "10111001" + _encode_reg(rA) + _encode_num(imm, 14)

# CMIM: Compare Immediate Multi Reg
def assemble_cmim(rA, imm, *args):
    return "10111101" + _encode_reg(rA) + _encode_num(imm, 14)

# CMM: Compare Multi Reg
def assemble_cmm(rA, rB, *args):
    return "10111100" + _encode_reg(rA) + _encode_reg(rB)

# CR: Call Register Conditional
def assemble_crn(rA, *args):
    return "110111" + "0000" + _encode_reg(rA) + "000"

def assemble_cre(rA, *args):
    return "110111" + "0001" + _encode_reg(rA) + "000"

def assemble_crl(rA, *args):
    return "110111" + "0010" + _encode_reg(rA) + "000"

def assemble_crle(rA, *args):
    return "110111" + "0011" + _encode_reg(rA) + "000"

def assemble_crg(rA, *args):
    return "110111" + "0100" + _encode_reg(rA) + "000"

def assemble_crge(rA, *args):
    return "110111" + "0101" + _encode_reg(rA) + "000"

def assemble_crno(rA, *args):
    return "110111" + "0110" + _encode_reg(rA) + "000"

def assemble_cro(rA, *args):
    return "110111" + "0111" + _encode_reg(rA) + "000"

def assemble_crns(rA, *args):
    return "110111" + "1000" + _encode_reg(rA) + "000"

def assemble_crs(rA, *args):
    return "110111" + "1001" + _encode_reg(rA) + "000"

def assemble_crsl(rA, *args):
    return "110111" + "1010" + _encode_reg(rA) + "000"

def assemble_crsle(rA, *args):
    return "110111" + "1011" + _encode_reg(rA) + "000"

def assemble_crsg(rA, *args):
    return "110111" + "1100" + _encode_reg(rA) + "000"

def assemble_crsge(rA, *args):
    return "110111" + "1101" + _encode_reg(rA) + "000"

def assemble_cr(rA, *args):
    return "110111" + "1111" + _encode_reg(rA) + "000"


# D
def assemble_dbrk():
    return "111111111111111111"

def assemble_di(rA):
    return "101000000101{}0".format(_encode_reg(rA))

def assemble_dmt(rA, rB, rC):
    return "0110100{}{}{}00000".format(_encode_reg(rA), _encode_reg(rB), _encode_reg(rC))

def assemble_dv(rA, rB, rC, *args):
    return "0001100{}{}{}0000{}".format(_encode_reg(rA), _encode_reg(rB), _encode_reg(rC), ("1" if len(args) else "0"))

def assemble_dvf(rA, rB, rC, *args):
    return "0001101{}{}{}0000{}".format(_encode_reg(rA), _encode_reg(rB), _encode_reg(rC), ("1" if len(args) else "0"))

def assemble_dvmf(rA, rB, rC, *args):
    return "0001111{}{}{}0000{}".format(_encode_reg(rA), _encode_reg(rB), _encode_reg(rC), ("1" if len(args) else "0"))

def assemble_dvi(rA, rB, imm, *args):
    return "0001100{}{}{}01{}".format(_encode_reg(rA), _encode_reg(rB), _encode_num(imm, 7), ("1" if len(args) else "0"))

def assemble_dvim(rA, rB, imm, *args):
    return "0001110{}{}{}01{}".format(_encode_reg(rA), _encode_reg(rB), _encode_num(imm, 7), ("1" if len(args) else "0"))

def assemble_dvis(rA, rB, imm, *args):
    return "0001100{}{}{}11{}".format(_encode_reg(rA), _encode_reg(rB), _encode_num(imm, 7), ("1" if len(args) else "0"))

def assemble_dvism(rA, rB, imm, *args):
    return "0001110{}{}{}11{}".format(_encode_reg(rA), _encode_reg(rB), _encode_num(imm, 7), ("1" if len(args) else "0"))

def assemble_dvm(rA, rB, rC, *args):
    return "0001110{}{}{}0000{}".format(_encode_reg(rA), _encode_reg(rB), _encode_reg(rC), ("1" if len(args) else "0"))

def assemble_dvs(rA, rB, rC, *args):
    return "0001100{}{}{}0010{}".format(_encode_reg(rA), _encode_reg(rB), _encode_reg(rC), ("1" if len(args) else "0"))

def assemble_dvsm(rA, rB, rC, *args):
    return "0001110{}{}{}0010{}".format(_encode_reg(rA), _encode_reg(rB), _encode_reg(rC), ("1" if len(args) else "0"))

# E

# EI: Enable Interrupts
def assemble_ei(rA, *args):
    """EDG"""
    return "101000000100" + _encode_reg(rA) + "0"

# F
def assemble_fti(rA, rB):
    return "101000101{}{}00000000".format(_encode_reg(rA), _encode_reg(rB))

def assemble_ftim(rA, rB):
    return "101000111{}{}00000000".format(_encode_reg(rA), _encode_reg(rB))
# H

def assemble_ht():
    return "101000000011000000"

# I
def assemble_ir():
    return "101000000001000000"

def assemble_itf(rA, rB):
    return "101000100{}{}00000000".format(_encode_reg(rA), _encode_reg(rB))

def assemble_itfm(rA, rB):
    return "101000110{}{}00000000".format(_encode_reg(rA), _encode_reg(rB))

# J

# K - there is no k

# L
# cub01d
def assemble_lds(rA, rB, offset, _regcount, mode="0"):
    return "1010100" + _encode_reg(rA) + _encode_reg(rB) + _encode_num(_regcount, 5) + \
             _encode_num(mode, 2) + _encode_offset(offset) + "000"
def assemble_ldsi(rA, rB, offset, _regcount):
    return assemble_lds(rA, rB, offset, _regcount, mode="1")
def assemble_ldsd(rA, rB, offset, _regcount):
    return assemble_lds(rA, rB, offset, _regcount, mode="2")

# iceboy
def assemble_ldt(rA, rB, offset, reg_count, mode="0"):
    return "1010110" + _encode_reg(rA) + _encode_reg(rB) + \
           _encode_reg_count(reg_count, 5) + _encode_num(mode, 2) + \
           _encode_offset(offset) + "000"

assemble_ldti = partial(assemble_ldt, mode="1")
assemble_ldtd = partial(assemble_ldt, mode="2")

# iceboy
def assemble_ldw(rA, rB, offset, reg_count, mode="0"):
    return "1010101" + _encode_reg(rA) + _encode_reg(rB) + \
           _encode_reg_count(reg_count, 5) + _encode_num(mode, 2) + \
           _encode_offset(offset) + "000"

assemble_ldwi = partial(assemble_ldw, mode="1")
assemble_ldwd = partial(assemble_ldw, mode="2")

# M

# MD: Modulus
def assemble_md(rA, rB, rC,  *args):
    return "0010000" + _encode_reg(rA) + _encode_reg(rB) + _encode_reg(rC) + "0000" + ("1" if len(args) else "0")

# MDF: Modulus Floating Point
def assemble_mdf(rA, rB, rC,  *args):
    return "0010001" + _encode_reg(rA) + _encode_reg(rB) + _encode_reg(rC) + "0000" + ("1" if len(args) else "0")

# MDFM: Modulus Floating Point Multi Reg
def assemble_mdf(rA, rB, rC,  *args):
    return "0010011" + _encode_reg(rA) + _encode_reg(rB) + _encode_reg(rC) + "0000" + ("1" if len(args) else "0")

# MDI: Modulus Immediate
def assemble_mdi(rA, rB, imm,  *args):
    return "0010000" + _encode_reg(rA) + _encode_reg(rB) + _encode_num(imm, 7) + "01" + ("1" if len(args) else "0")

# MDIM: Modulus Immediate Multi Reg
def assemble_mdim(rA, rB, imm,  *args):
    return "0010010" + _encode_reg(rA) + _encode_reg(rB) + _encode_num(imm, 7) + "01" + ("1" if len(args) else "0")

# MDIS: Modulus Immediate Signed
def assemble_mdis(rA, rB, imm,  *args):
    return "0010000" + _encode_reg(rA) + _encode_reg(rB) + _encode_num(imm, 7) + "11" + ("1" if len(args) else "0")

# MDISM: Modulus Immediate Signed Multi Reg
def assemble_mdism(rA, rB, imm,  *args):
    return "0010010" + _encode_reg(rA) + _encode_reg(rB) + _encode_num(imm, 7) + "11" + ("1" if len(args) else "0")

# MDM: Modulus Multi Reg
def assemble_mdm(rA, rB, rC,  *args):
    return "0010010" + _encode_reg(rA) + _encode_reg(rB) + _encode_reg(rC) + "0000" + ("1" if len(args) else "0")

# MDS: Modulus Signed
def assemble_mds(rA, rB, rC,  *args):
    return "0010000" + _encode_reg(rA) + _encode_reg(rB) + _encode_reg(rC) + "0010" + ("1" if len(args) else "0")

# MDSM: Modulus Signed Multi Reg
def assemble_mdsm(rA, rB, rC,  *args):
    return "0010010" + _encode_reg(rA) + _encode_reg(rB) + _encode_reg(rC) + "0010" + ("1" if len(args) else "0")

def assemble_mh(rA, imm, *args):
    return '10001' + _encode_reg(rA) + _encode_num(imm, 17)

def assemble_ml(rA, imm, *args):
    return '10010' + _encode_reg(rA) + _encode_num(imm, 17)

def assemble_mi(rA, imm, *args):
    imm = _encode_num(imm, 27).zfill(27)
    #print "IMMEDIATE: %d %s", imm
    #print '0b'+imm[-9:]
    #print '0b'+imm[:-9]
    return assemble_ml(rA, '0b'+imm[-10:]) + assemble_mh(rA, '0b'+imm[:-10])

def assemble_ms(rA, imm, *args):
    return '10011' + _encode_reg(rA) + _encode_num(imm, 17)

def assemble_mu(rA, rB, rC, *args):
    return '0001000' + _encode_reg(rA) + _encode_reg(rB) + _encode_reg(rC) + '0000' + ("1" if len(args) else "0")

def assemble_muf(rA, rB, rC, *args):
    return '0001001' + _encode_reg(rA) + _encode_reg(rB) + _encode_reg(rC) + '0000' + ("1" if len(args) else "0")

def assemble_mufm(rA, rB, rC, *args):
    return '0001011' + _encode_reg(rA) + _encode_reg(rB) + _encode_reg(rC) + '0000' + ("1" if len(args) else "0")

def assemble_mui(rA, rB, imm, *args):
    return '0001000' + _encode_reg(rA) + _encode_reg(rB) + _encode_num(imm, 7) + '01' + ("1" if len(args) else "0")

def assemble_muim(rA, rB, imm, *args):
    return '0001010' + _encode_reg(rA) + _encode_reg(rB) + _encode_num(imm, 7) + '01' + ("1" if len(args) else "0")

def assemble_muis(rA, rB, imm, *args):
    return '0001000' + _encode_reg(rA) + _encode_reg(rB) + _encode_num(imm, 7) + '11' + ("1" if len(args) else "0")

def assemble_muism(rA, rB, imm, *args):
    return '0001010' + _encode_reg(rA) + _encode_reg(rB) + _encode_num(imm, 7) + '11' + ("1" if len(args) else "0")

def assemble_mum(rA, rB, rC, *args):
    return '0001010' + _encode_reg(rA) + _encode_reg(rB) + _encode_reg(rC) + '0000' + ("1" if len(args) else "0")

def assemble_mus(rA, rB, rC, *args):
    return '0001000' + _encode_reg(rA) + _encode_reg(rB) + _encode_reg(rC) + '0010' + ("1" if len(args) else "0")

def assemble_musm(rA, rB, rC, *args):
    return '0001010' + _encode_reg(rA) + _encode_reg(rB) + _encode_reg(rC) + '0010' + ("1" if len(args) else "0")

# N

# jmgrosen
def assemble_ng(rA, rB, *args):
    return "101001100" + _encode_reg(rA) + _encode_reg(rB) + "0000000" + ("1" if len(args) else "0")

# jmgrosen
def assemble_ngf(rA, rB, *args):
    return "101001101" + _encode_reg(rA) + _encode_reg(rB) + "0000000" + ("1" if len(args) else "0")

# jmgrosen
def assemble_ngfm(rA, rB, *args):
    return "101001111" + _encode_reg(rA) + _encode_reg(rB) + "0000000" + ("1" if len(args) else "0")

# jmgrosen
def assemble_ngm(rA, rB, *args):
    return "101001110" + _encode_reg(rA) + _encode_reg(rB) + "0000000" + ("1" if len(args) else "0")

# jmgrosen
def assemble_nt(rA, rB, *args):
    return "101001100" + _encode_reg(rA) + _encode_reg(rB) + "0100000" + ("1" if len(args) else "0")

# jmgrosen
def assemble_ntm(rA, rB, *args):
    return "101001110" + _encode_reg(rA) + _encode_reg(rB) + "0100000" + ("1" if len(args) else "0")


# O


def assemble_or(rA, rB, rC, *args):
    "Fish"
    return "0011000" + _encode_reg(rA) + _encode_reg(rB) + _encode_reg(rC) + "0000" + ("1" if len(args) else "0")


def assemble_ori(rA, rB, imm, *args):
    "Fish"
    return "0011000" + _encode_reg(rA) + _encode_reg(rB) + _encode_num(imm, 7) + "01" + ("1" if len(args) else "0")


def assemble_orm(rA, rB, rC, *args):
    "Fish"
    return "0011010" + _encode_reg(rA) + _encode_reg(rB) + _encode_reg(rC) + "0000" + ("1" if len(args) else "0")


# P - there is no p

# Q - there is no q

# R

def assemble_re():
    return "101000000000000000"

def assemble_rf(rA):
    return "101000001100" + _encode_reg(rA) + "0"

def assemble_rl(rA, rB, rC, *args):
    return "0110000" + _encode_reg(rA) + _encode_reg(rB) + _encode_reg(rC) + "0000" + ("1" if len(args) else "0")

def assemble_rli(rA, rB, imm, *args):
    return "1000000" + _encode_reg(rA) + _encode_reg(rB) + _encode_num(imm, 7) + "00" + ("1" if len(args) else "0")

def assemble_rlim(rA, rB, imm, *args):
    return "1000010" + _encode_reg(rA) + _encode_reg(rB) + _encode_num(imm, 7) + "00" + ("1" if len(args) else "0")

def assemble_rlm(rA, rB, rC, *args):
    return "0110010" + _encode_reg(rA) + _encode_reg(rB) + _encode_reg(rC) + "0000" + ("1" if len(args) else "0")

def assemble_rmp(rA, rB):
    return "1010010" + _encode_reg(rA) + _encode_reg(rB) + "0000000000"

def assemble_rnd(rA, *args):
    return "101001100" + _encode_reg(rA) + "000001100000" + ("1" if len(args) else "0")

def assemble_rri(rA, rB, imm, *args):
    return "1000001" + _encode_reg(rA) + _encode_reg(rB) + _encode_num(imm, 7) + "00" + ("1" if len(args) else "0")

def assemble_rrim(rA, rB, imm, *args):
    return "1000011" + _encode_reg(rA) + _encode_reg(rB) + _encode_num(imm, 7) + "00" + ("1" if len(args) else "0")

def assemble_rrm(rA, rB, rC, *args):
    return "0110011" + _encode_reg(rA) + _encode_reg(rB) + _encode_reg(rC) + "0000" + ("1" if len(args) else "0")
# S


def assemble_sa(rA, rB, rC, *args):
    return '0101101' + _encode_reg(rA) + _encode_reg(rB) + _encode_reg(rC) + '0000' + ('1' if len(args) else '0')

def assemble_sai(rA, rB, imm, *args):
    return '0111101' + _encode_reg(rA) + _encode_reg(rB) + _encode_num(imm, 7) + '00' + ('1' if len(args) else '0')

def assemble_saim(rA, rB, imm, *args):
    return '0111111' + _encode_reg(rA) + _encode_reg(rB) + _encode_num(imm, 7) + '00' + ('1' if len(args) else '0')

def assemble_sam(rA, rB, rC, *args):
    return '0101111' + _encode_reg(rA) + _encode_reg(rB) + _encode_reg(rC) + '0000' + ('1' if len(args) else '0')

def assemble_sb(rA, rB, rC, *args):
    return '0000100' + _encode_reg(rA) + _encode_reg(rB) + _encode_reg(rC) + '0000' + ('1' if len(args) else '0')

def assemble_sbc(rA, rB, rC, *args):
    return '0100100' + _encode_reg(rA) + _encode_reg(rB) + _encode_reg(rC) + '0000' + ('1' if len(args) else '0')

def assemble_sbci(rA, rB, imm, *args):
    return '0100100' + _encode_reg(rA) + _encode_reg(rB) + _encode_num(imm, 7) + '01' + ('1' if len(args) else '0')

def assemble_sbcim(rA, rB, imm, *args):
    return '0100110' + _encode_reg(rA) + _encode_reg(rB) + _encode_num(imm, 7) + '01' + ('1' if len(args) else '0')

def assemble_sbcm(rA, rB, rC, *args):
    return '0100110' + _encode_reg(rA) + _encode_reg(rB) + _encode_reg(rC) + '0000' + ('1' if len(args) else '0')

def assemble_sbf(rA, rB, rC, *args):
    return '0000101' + _encode_reg(rA) + _encode_reg(rB) + _encode_reg(rC) + '0000' + ('1' if len(args) else '0')

def assemble_sbfm(rA, rB, rC, *args):
    return '0000111' + _encode_reg(rA) + _encode_reg(rB) + _encode_reg(rC) + '0000' + ('1' if len(args) else '0')

def assemble_sbi(rA, rB, imm, *args):
    return '0000100' + _encode_reg(rA) + _encode_reg(rB) + _encode_num(imm, 7) + '01' + ('1' if len(args) else '0')

def assemble_sbim(rA, rB, imm, *args):
    return '0000110' + _encode_reg(rA) + _encode_reg(rB) + _encode_num(imm, 7) + '01' + ('1' if len(args) else '0')

def assemble_sbm(rA, rB, rC, *args):
    return '0000110' + _encode_reg(rA) + _encode_reg(rB) + _encode_reg(rC) + '0000' + ('1' if len(args) else '0')

def assemble_ses(rA, rB, *args):
    return '101000000111' + _encode_reg(rA) + _encode_reg(rB) + '00000'

def assemble_sew(rA, rB, *args):
    return '101000001000' + _encode_reg(rA) + _encode_reg(rB) + '00000'

def assemble_sf(rA, *args):
    return '101000001011' + _encode_reg(rA) + '0'

def assemble_sl(rA, rB, rC, *args):
    return '0101000' + _encode_reg(rA) + _encode_reg(rB) + _encode_reg(rC) + '0000' + ('1' if len(args) else '0')

def assemble_sli(rA, rB, imm, *args):
    return '0111000' + _encode_reg(rA) + _encode_reg(rB) + _encode_num(imm, 7) + '00' + ('1' if len(args) else '0')

def assemble_slim(rA, rB, imm, *args):
    return '0111010' + _encode_reg(rA) + _encode_reg(rB) + _encode_num(imm, 7) + '00' + ('1' if len(args) else '0')

def assemble_slm(rA, rB, rC, *args):
    return '0101010' + _encode_reg(rA) + _encode_reg(rB) + _encode_reg(rC) + '0000' + ('1' if len(args) else '0')

def assemble_smp(rA, rB, flagz):
    return '1010010' + _encode_reg(rA) + _encode_reg(rB) + '1' + _encode_num(flagz, 2) + '0000000'

def assemble_sr(rA, rB, rC, *args):
    return '0101001' + _encode_reg(rA) + _encode_reg(rB) + _encode_reg(rC) + '0000' + ('1' if len(args) else '0')

def assemble_sri(rA, rB, imm, *args):
    return '0111001' + _encode_reg(rA) + _encode_reg(rB) + _encode_num(imm, 7) + '00' + ('1' if len(args) else '0')

def assemble_srim(rA, rB, imm, *args):
    return '0111011' + _encode_reg(rA) + _encode_reg(rB) + _encode_num(imm, 7) + '00' + ('1' if len(args) else '0')


def assemble_srm(rA, rB, rC, *args):
    "Fish"
    return "0101011" + _encode_reg(rA) + _encode_reg(rB) + _encode_reg(rC) + "0000" + ("1" if len(args) else "0")

def assemble_sts(rA, rB, offset, reg_count):
    "Fish"
    return "1011000" + _encode_reg(rA) + _encode_reg(rB) + _encode_reg_count(reg_count, 5) + "00" + \
           _encode_offset(offset) + "000"

def assemble_stsi(rA, rB, offset, reg_count):
    "Fish"
    return "1011000" + _encode_reg(rA) + _encode_reg(rB) + _encode_reg_count(reg_count, 5) + "01" + \
           _encode_offset(offset) + "000"

def assemble_stsd(rA, rB, offset, reg_count):
    "Fish"
    return "1011000" + _encode_reg(rA) + _encode_reg(rB) + _encode_reg_count(reg_count, 5) + "10" + \
           _encode_offset(offset) + "000"

def assemble_stt(rA, rB, offset, reg_count):
    "Fish"
    return "1011010" + _encode_reg(rA) + _encode_reg(rB) + _encode_reg_count(reg_count, 5) + "00" + \
           _encode_offset(offset) + "000"

def assemble_sttl(rA, rB, offset, reg_count):
    "Fish"
    return "1011010" + _encode_reg(rA) + _encode_reg(rB) + _encode_reg_count(reg_count, 5) + "01" + \
           _encode_offset(offset) + "000"

def assemble_sttd(rA, rB, offset, reg_count):
    "Fish"
    return "1011010" + _encode_reg(rA) + _encode_reg(rB) + _encode_reg_count(reg_count, 5) + "10" + \
           _encode_offset(offset) + "000"

def assemble_stw(rA, rB, offset, reg_count):
    "Fish"
    return "1011001" + _encode_reg(rA) + _encode_reg(rB) + _encode_reg_count(reg_count, 5) + "00" + \
           _encode_offset(offset) + "000"

def assemble_stwl(rA, rB, offset, reg_count):
    "Fish"
    return "1011001" + _encode_reg(rA) + _encode_reg(rB) + _encode_reg_count(reg_count, 5) + "01" + \
           _encode_offset(offset) + "000"

def assemble_stwd(rA, rB, offset, reg_count):
    "Fish"
    return "1011001" + _encode_reg(rA) + _encode_reg(rB) + _encode_reg_count(reg_count, 5) + "10" + \
           _encode_offset(offset) + "000"




# T
# No instruction starts with T

# U

# V

# W


def assemble_wt(*args):
    "Fish"
    return "101000000010000000"


# X


def assemble_xr(rA, rB, rC, *args):
    "Fish"
    return "0011100" + _encode_reg(rA) + _encode_reg(rB) + _encode_reg(rC) + "0000" + ("1" if len(args) else "0")


def assemble_xri(rA, rB, imm, *args):
    "Fish"
    return "0011100" + _encode_reg(rA) + _encode_reg(rB) + _encode_num(imm, 7) + "01" + ("1" if len(args) else "0")


def assemble_xrm(rA, rB, rC, *args):
    "Fish"
    return "0011110" + _encode_reg(rA) + _encode_reg(rB) + _encode_reg(rC) + "0000" + ("1" if len(args) else "0")


# Y

# Z

def assemble_zes(rA, rB, *args):
    "Fish"
    return "101000001001" + _encode_reg(rA) + _encode_reg(rB) + "00000"


def assemble_zew(rA, rB, *args):
    "Fish"
    return "101000001010" + _encode_reg(rA) + _encode_reg(rB) + "00000"

#
# ADD HANDLERS ABOVE HERE
#

def do_label(label):
    global pc
    if label in labels and labels[label] != pc:
        logger.warning("label '%s' already defined differently, overriding", label)
    labels[label] = pc
    return ""

PARSE_RULES = [
    (r"(?P<label>\w+)\s*:$", do_label),
]

def assemble_instruction(line):
    global pc

    line = line.split(";")[0].strip()  # supports comments
    if not line:
        return ''

    # special parsing rules
    for pattern, action in PARSE_RULES:
        match = re.match(pattern, line)
        if match:
            a = action(**match.groupdict())
            break
    else:
        line = re.sub(r"\[\s*([^,\+]*?)\s*\]", r"[\1 + 0, 1]", line)
        line = re.sub(r"\[\s*([^,\+]*?)\s*,\s*([^,\+]*?)\s*\]", r"[\1 + 0, \2]", line)
        line = re.sub(r"\[\s*([^,\+]*?)\s*\+\s*([^,\+]*?)\s*\]", r"[\1 + \2, 1]", line)

        # default parsing rule: ignore brackets, comma and plus sign, and split by space
        line = re.sub('[\\[\\]+,]', ' ', line)

        parts = line.split()
        op = parts[0]
        args = parts[1:]
        if op.endswith("."):
            args.append("UL")
            op = op.strip('.')

        if line.startswith(".db"): #bits
            assert len(parts[1]) % 9 == 0
            for ch in parts[1]:
                assert ch == '0' or ch == '1'
            return parts[1]
        elif line.startswith(".dn"): #nyte
            return _encode_num(parts[1], 9)
        elif line.startswith(".dt"): #tri
            return _encode_num(parts[1], 27)

        try:
            assembler = globals()['assemble_'+op.lower()]
        except KeyError:
            raise Exception("Unsupported instruction: %s" % op)
        a = assembler(*args)

    assert len(a) % 9 == 0
    pc += (len(a) / 9)
    return encode_me(a)

def assemble_instructions(lines):
    global first_pass
    global pc

    # two pass for labels
    first_pass = True
    pc = 0
    for line in lines:
        assemble_instruction(line)
    first_pass = False
    pc = 0
    return to_bin("".join(map(assemble_instruction, lines)))

def random_test(n=100):
    from disassemble_single import get_disassembled
    from random import choice
    from os import urandom

    for i in xrange(n):
        valid = False
        while not valid:
            byte_len = choice([18, 27, 36, 54]) / 9
            data = urandom(byte_len)
            ret = get_disassembled(data)
            if ret.startswith("Error"):
                continue
            try:
                ours = to_bin(assemble_instruction(ret))
                ours_disassembled = get_disassembled(ours)
            except Exception as e:
                print "ERROR"
                print "While assembling %r:" % ret
                print "Original was %r" % data
                print "But encountered error while assembling:"
                raise
            if ours_disassembled != ret:
                print "ERROR"
                print "While assembling %r:" % ret
                print "Original was %r" % data
                print "but we wrote %r" % ours
                print "Ours disasms to: %r" % get_disassembled(ours)
                return False
            print "GOOD: %r" % ret
            valid = True
    return True

if __name__ == "__main__":
    logging.basicConfig()
    if len(sys.argv) == 3:
        assembled = assemble_instructions(open(sys.argv[1]).readlines())
        open(sys.argv[2], 'w').write(assembled)
    else:
        random_test(int(sys.argv[1]) if len(sys.argv) == 2 else 100)
