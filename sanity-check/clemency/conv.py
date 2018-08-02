import logging


l = logging.getLogger("conv")

def bytes_to_nytes(b):
    bin_str = "".join(bin(ord(c))[2:].zfill(9) for c in b)
    bin_str = bin_str.ljust(len(bin_str) + ((8 - (len(bin_str) % 8)) % 8), "0")
    return "".join(chr(int(bin_str[i:i+8], 2)) for i in xrange(0, len(bin_str), 8))

def nytes_to_array(n):
    bin_str = nytes_to_bit_string(n)
    return [int(bin_str[i:i+9], 2) for i in xrange(0, len(bin_str), 9)]

def nytes_to_array_right_aligned(n):
    bin_str = "".join(bin(ord(c))[2:].zfill(8) for c in n)
    num_bits = (len(n) * 8) % 9
    bin_str = bin_str[num_bits:]
    return [int(bin_str[i:i+9], 2) for i in xrange(len(bin_str) - 9, -9, -9)]

def array_to_nytes(a):
    bin_str = "".join(bin(e)[2:].zfill(9) for e in a)
    bin_str = bin_str.ljust(len(bin_str) + ((8 - (len(bin_str) % 8)) % 8), '0')
    return "".join(chr(int(bin_str[i:i+8], 2)) for i in xrange(0, len(bin_str), 8))

def nytes_to_bytes(n):
    return "".join(chr(c) for c in nytes_to_array(n))

def middle_endian_array_ack(a):
    if len(a) == 2:
        return a[::-1]
    elif len(a) == 3:
        return a[:2][::-1] + [a[2]]
    elif len(a) == 4:
        return a[:2][::-1] + a[2:4]
    elif len(a) == 6:
        return a[0:2][::-1] + [a[2]] + a[3:5][::-1] + [a[5]]
    raise ValueError("I have no clue what format %d-byte things are in. Let @paul know and I'll add it." % len(a))

def middle_endian_nytes_unpack(n):
    return sum(v << (i * 9) for i, v in enumerate(middle_endian_array_ack(nytes_to_array_right_aligned(n)[::-1])[::-1]))

def middle_endian_bytes_unpack(b):
    l.warning("are you sure you want to use this? I don't know why you'd have a byte and middle-endian encoded string . . .")
    return sum(v << (i * 8) for i, v in enumerate(middle_endian_array_ack([ord(c) for c in b][::-1])))

def middle_endian_nytes_pack_2(i):
    return array_to_nytes(middle_endian_array_ack([(i & (0x1FF << (v * 9))) >> (v * 9) for v in xrange(2)][::-1]))

def middle_endian_nytes_pack_3(i):
    return array_to_nytes(middle_endian_array_ack([(i & (0x1FF << (v * 9))) >> (v * 9) for v in xrange(3)][::-1]))

def middle_endian_nytes_pack_6(i):
    return array_to_nytes(middle_endian_array_ack([(i & (0x1FF << (v * 9))) >> (v * 9) for v in xrange(6)][::-1]))

def middle_endian_nytes_bit_string(s):
    return "".join(middle_endian_array_ack([s[i:i+9] for i in xrange(0, len(s), 9)]))

def nytes_to_bit_string(n):
    bin_str = "".join(bin(ord(c))[2:].zfill(8) for c in n)
    num_bits = (len(n) * 8) % 9
    return bin_str[:len(bin_str) - num_bits]

def bit_string_to_data(s):
    bin_str = s.ljust((len(s) + 7) & (~7))
    return "".join(chr(int(bin_str[i:i + 8], 2)) for i in xrange(0, len(bin_str), 8))
