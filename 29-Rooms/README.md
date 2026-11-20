# Rooms

| | |
|---|---|
| **Categoría** | Reversing |
| **Dificultad** | Media |
| **Puntos** | 250 |
| **Reto #** | 29 |

## Descripción

Un explorador recorre 10 salas. Cada sala (`room_01`–`room_10`) decodifica un fragmento de la flag con una técnica distinta (XOR, Base64, ROT13, hex, NOT, resta, suma, rotr8) y lo concatena en un buffer. El programa nunca llama a `printf`/`puts` con el resultado.

## Vulnerabilidad

**10 codificaciones encadenadas en funciones separadas** — el binario no está stripped; los nombres de funciones (`rotr8`, `rot13c`, `b64decode`, `hexval`) identifican cada técnica sin ejecutar nada.

## Análisis

| Sala | Técnica | Resultado |
|------|---------|-----------|
| room_01 | XOR 0x5a | TH |
| room_02 | Resta 0x10 a cada byte | .e |
| room_03 | Base64 (b64decode) | xp |
| room_04 | Inversión de los 2 bytes | l0 |
| room_05 | XOR con índice i | r4 |
| room_06 | ROT13 (rot13c) | nd |
| room_07 | NOT bit a bit (~byte) | 0_ |
| room_08 | Hexadecimal (hexval) | s4 |
| room_09 | Rotación derecha 3 bits (rotr8) | l4 |
| room_10 | Suma 0x25 a cada byte | s. |

## Solución

```python
import base64

def rotr8(b, n):
    b &= 0xff; n &= 7
    return ((b >> n) | (b << (8 - n))) & 0xff

def rot13c(c):
    if 97 <= c <= 122: return (c - 97 + 13) % 26 + 97
    if 65 <= c <= 90:  return (c - 65 + 13) % 26 + 65
    return c

# Datos cifrados extraídos de .rodata con objdump -s -j .rodata rooms
r1 = bytes([0x0e, 0x12]);                    p1 = bytes(b ^ 0x5a for b in r1)
r2 = bytes([0x8b, 0x75]);                    p2 = bytes(b - 0x10 & 0xff for b in r2)
r3 = b"eHA=";                                p3 = base64.b64decode(r3)
r4 = bytes([0x30, 0x6c]);                    p4 = bytes(reversed(r4))
r5 = bytes([0x72, 0x35]);                    p5 = bytes(b ^ i for i, b in enumerate(r5))
r6 = bytes([0x61, 0x71]);                    p6 = bytes(rot13c(b) for b in r6)
r7 = bytes([0xcf, 0xa0]);                    p7 = bytes(~b & 0xff for b in r7)
r8 = b"7334";                               p8 = bytes.fromhex(r8.decode())
r9 = bytes([0x63, 0xa1]);                    p9 = bytes(rotr8(b, 3) for b in r9)
r10 = bytes([0x4e, 0x58]);                   p10 = bytes(b + 0x25 & 0xff for b in r10)

flag = (p1+p2+p3+p4+p5+p6+p7+p8+p9+p10).decode()
print(flag)
```

> 🚩 **Flag:** omitida intencionalmente. Seguí los pasos para obtenerla.

## Takeaways

- Cada técnica encadenada es independiente — atacar sala por sala en lugar de buscar la inversión global.
- Símbolos no stripped como `b64decode`, `rot13c`, `hexval` identifican la técnica instantáneamente.
- `objdump -s -j .rodata` extrae todos los datos cifrados de una sola vez.

---
*Tropical Hunters CTF — Writeup por [Fabián Bustamante](https://github.com/fbustamante55)*
