# One Byte

| | |
|---|---|
| **Categoría** | Crypto |
| **Dificultad** | Fácil |
| **Puntos** | 50 |
| **Reto #** | 35 |

## Descripción

`message.txt` contiene un hex dump cifrado con XOR. La pista: *"La llave es bastante corta."* Una clave de 1 byte tiene solo 256 posibilidades.

## Vulnerabilidad

**XOR de 1 byte — fuerza bruta trivial** — con 256 posibilidades y el prefijo conocido `TH{`, la clave se determina en microsegundos.

## Solución

### Opción A — Fuerza bruta completa

```python
ct = bytes.fromhex(
    "d3f0f2fae4e1b1f2fefce1fdf4e5f4f5b1f0e5b1a1a3aba1a1bfb1"
    "dff4e9e5b1faf4e8b1e3fee5f0e5f8feffb1f8ffb1a2a1b1f5f0"
    "e8e2bfb1d0f2f2f4e2e2b1f2fef5f4abb1c5d9eaa3a4a7cee5e3"
    "a0a2e2cea0e2ceffa1e5f9a0fff6ec"
)

for key in range(256):
    pt = bytes(b ^ key for b in ct)
    if b"TH{" in pt:
        print(f"[+] Clave: 0x{key:02x}")
        print(pt.decode(errors="ignore"))
        break
```

### Opción B — Known plaintext (1 operación)

```python
# ct[0] ^ 0x54 ('T') = clave
key = ct[0] ^ 0x54   # 0x91
print(bytes(b ^ key for b in ct).decode())
```

> 🚩 **Flag:** omitida intencionalmente. Seguí los pasos para obtenerla.

## Takeaways

- XOR de 1 byte: 256 candidatos, fuerza bruta en < 1 ms.
- Known plaintext attack: `clave = ciphertext[0] ^ plaintext[0]` — una sola operación.
- Una clave de 1 byte no ofrece seguridad real, independientemente de la longitud del mensaje.

---
*Tropical Hunters CTF — Writeup por [Fabián Bustamante](https://github.com/fbustamante55)*
