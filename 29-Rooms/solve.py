#!/usr/bin/env python3
# Solucion: Rooms (Reversing)
# El programa arma la flag llamando a room_01..room_10 en orden,
# cada una decodifica su propio trozo de .rodata con una tecnica
# distinta (XOR, resta, base64, inversion de bytes, XOR con indice,
# ROT13, NOT bit a bit, hex, rotacion de bits, suma). El resultado
# solo se usa para animar una grilla ASCII; nunca se imprime.
import base64

def rotr8(b, n):
    b &= 0xff
    n &= 7
    return ((b >> n) | (b << (8 - n))) & 0xff

def rot13c(c):
    if 97 <= c <= 122:
        return (c - 97 + 13) % 26 + 97
    if 65 <= c <= 90:
        return (c - 65 + 13) % 26 + 65
    return c

e9 = bytes([0x0e, 0x12])
e8 = bytes([0x8b, 0x75])
e7 = b"eHA="
e6 = bytes([0x30, 0x6c])
e5 = bytes([0x72, 0x35])
e4 = bytes([0x61, 0x71])
e3 = bytes([0xcf, 0xa0])
e2 = b"7334"
e1 = bytes([0x63, 0xa1])
e0 = bytes([0x4e, 0x58])

room_01 = bytes(b ^ 0x5a for b in e9)
room_02 = bytes((b - 0x10) & 0xff for b in e8)
room_03 = base64.b64decode(e7)
room_04 = bytes([e6[1], e6[0]])
room_05 = bytes(b ^ i for i, b in enumerate(e5))
room_06 = bytes(rot13c(b) for b in e4)
room_07 = bytes((~b) & 0xff for b in e3)
room_08 = bytes.fromhex(e2.decode())
room_09 = bytes(rotr8(b, 3) for b in e1)
room_10 = bytes((b + 0x25) & 0xff for b in e0)

flag = b"".join([room_01, room_02, room_03, room_04, room_05,
                  room_06, room_07, room_08, room_09, room_10])
print(flag.decode())
