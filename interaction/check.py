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
        print "Choosing from:", can_control
        arch = random.choice(list(can_control))
    print "Firing against", arch
    if backdoor:
        r.sendline(secret_phrase)
        send_shellcode(r, arch)
    r.sendline(arch)
    output = r.readuntil("Checking for control...", timeout=10)
    print output or r.readrepeat(timeout=1)
    now_control = parse_controlled(r)
    assert now_control == do_control | { arch }
    return now_control


def full_control(host, port, target_control=max_control):
    controlled = set()
    first_arch = random.choice(list(available['present']))
    print "First arch:", first_arch

    r = pwn.remote(host, port)
    send_shellcode(r, first_arch)

    print r.readuntil('ready.\n> ')
    r.send('\n')

    # fire present
    if target_control >= 1:
        babble = r.readuntil("> ")
        can_control = parse_status(babble)
        assert set(can_control) == available['present']
        controlled = fire_arch(r, controlled, can_control, arch=first_arch, backdoor=False)

    # fire past
    if target_control >= 2:
        babble = r.readuntil("> ")
        can_control = parse_status(babble)
        assert set(can_control) == available['past']
        controlled = fire_arch(r, controlled, can_control)

    # fire future
    if target_control >= 3:
        babble = r.readuntil("> ")
        can_control = parse_status(babble)
        assert set(can_control) == (available['past'] | available['future']) - controlled
        controlled = fire_arch(r, controlled, can_control)

    while len(controlled) < target_control:
        babble = r.readuntil("> ")
        can_control = parse_status(babble)
        assert set(can_control) == (available['past'] | available['future']) - controlled
        controlled = fire_arch(r, controlled, can_control)

    r.sendline("DONE")

    o = r.readrepeat(timeout=1)
    assert ("control over %d" % target_control) in o
    print o

def main():
    host = sys.argv[1]
    port = int(sys.argv[2])
    for i in range(max_control + 1):
        print "TRYING:",i
        full_control(host, port, target_control=i)

    print "DONE"
    sys.exit(0)

if __name__ == '__main__':
    main()
