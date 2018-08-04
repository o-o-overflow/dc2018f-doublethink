#!/usr/bin/env python2

import random
import pwn #pylint:disable=import-error
import sys
import os

available = {
        'past': { 'lgp-30', 'pdp-1', 'pdp-8', 'pdp-10', 'mix', 'ibm-1401', 'nova' },
        'present': { 'amd64', 'arm64', 'mipsel' },
        'future': { 'risc-v', 'hexagon', 'mmix', 'clemency' }
}
all_available = set.union(*available.values())
max_control = len(available['past']) + len(available['future']) + 1

secret_phrase = "this is a super secret phrase that will allow us to test arbitrary solution combinations"

def send_shellcode(r, archname):
    r.readuntil('Shellcode length:\n')
    r.readuntil('> ')
    shellcode = open(os.path.join(os.path.dirname(__file__), 'platforms', archname, 'shellcode'), 'r').read()
    r.sendline(str(len(shellcode)))
    r.send(shellcode)

def parse_status(status):
    print status
    control_lines = [ line for line in status.split('\n') if 'architectures' in line and ':' in line and ('past' in line or 'present' in line or 'future' in line) ]
    assert control_lines
    arches = set.union(*[set(line.split(":",2)[1].split()) for line in control_lines])
    print "Available architectures:", arches
    assert arches < all_available
    return arches

def parse_controlled(r):
    print r.readuntil("You control: ")
    now_control = r.readuntil('\n').split()
    print now_control
    return set(now_control)

def fire_arch(r, do_control, can_control, arch=None, backdoor=True):
    if not arch:
        arch = random.choice(list(can_control))
    if backdoor:
        r.sendline(secret_phrase)
        send_shellcode(r, arch)
    r.sendline(arch)
    print r.readuntil("Checking for control...")
    now_control = parse_controlled(r)
    assert now_control == do_control | { arch }
    return now_control


def full_control(host, port):
    controlled = set()
    first_arch = random.choice(list(available['present']))
    print "First arch:", first_arch

    r = pwn.remote(host, port)
    send_shellcode(r, first_arch)

    print r.readuntil('ready.\n> ')
    r.send('\n')

    # fire present
    babble = r.readuntil("> ")
    can_control = parse_status(babble)
    assert set(can_control) == available['present']
    controlled = fire_arch(r, controlled, can_control, arch=first_arch, backdoor=False)

    # fire past
    babble = r.readuntil("> ")
    can_control = parse_status(babble)
    assert set(can_control) == available['past']
    controlled = fire_arch(r, controlled, can_control)

    # fire future
    babble = r.readuntil("> ")
    can_control = parse_status(babble)
    assert set(can_control) == (available['past'] | available['future']) - controlled
    controlled = fire_arch(r, controlled, can_control)

    while len(controlled) < max_control:
        controlled = fire_arch(r, controlled, can_control)

    sys.exit(0)

def main():
    host = sys.argv[1]
    port = int(sys.argv[2])
    full_control(host, port)

if __name__ == '__main__':
    main()
