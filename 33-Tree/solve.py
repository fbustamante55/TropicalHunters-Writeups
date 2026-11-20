#!/usr/bin/env python3
# Solucion: Tree (Reversing)
# main() solo llama a stage1..stage4 si argc > 9999, y encima las
# invoca con argumentos en 0, asi que los chequeos de registro nunca
# pasan en un uso normal. Hay que saltar a cada stage con un
# depurador (gdb) y poner los registros en los valores que esperan.
# Esto solo reconstruye los fragmentos (XOR 0x5a) a partir de .rodata.

def dec(hexstr):
    return bytes(b ^ 0x5a for b in bytes.fromhex(hexstr)).decode()

# stage1() -- sin chequeo, se ejecuta siempre -> enc.3
part1 = dec("0e122129" + "6e")
# stage2(edi == 0x1337) -> enc.2
part2 = dec("362e6e05" + "23")
# stage3(edi == 0xbeef) -> enc.1
part3 = dec("052a6e28" + "39")
# stage4(edi == 0xa, esi == 0xb) -> enc.0
part4 = dec("32696e27")

flag = part1 + part2 + part3 + part4
print(flag)

# En GDB (con el binario cargado y detenido antes de que acabe main):
#   break main
#   run
#   call (int)stage1()
#   call (int)stage2(0x1337)
#   call (int)stage3(0xbeef)
#   call (int)stage4(0xa, 0xb)
