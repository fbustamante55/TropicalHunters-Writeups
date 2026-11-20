#!/usr/bin/env python3
# Solución: Robot (Reversing)
# Cada parte de la flag esta en .rodata, cifrada con XOR de 1 byte,
# y la clave de cada parte esta hardcodeada al inicio de su funcion
# (part_a..part_d). El binario arma la flag en memoria (assemble_flag)
# pero solo la usa para animar el dibujo del robot; nunca la imprime.

chunks = [
    (bytes.fromhex("475b6843"), 0x13),  # part_a <- enc.4
    (bytes.fromhex("13555354"), 0x27),  # part_b <- enc.3
    (bytes.fromhex("15097b3a"), 0x4a),  # part_c <- enc.2
    (bytes.fromhex("05081f10"), 0x6d),  # part_d <- enc.1
]

flag = b"".join(bytes(b ^ key for b in enc) for enc, key in chunks)
print(flag.decode())
