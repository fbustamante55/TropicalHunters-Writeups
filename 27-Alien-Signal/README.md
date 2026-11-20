# Alien Signal

| | |
|---|---|
| **Categoría** | Reversing |
| **Dificultad** | Fácil |
| **Puntos** | 100 |
| **Reto #** | 27 |

## Descripción

Una transmisión alienígena cifrada con XOR. Los bytes en memoria ya están cifrados; el mensaje original no está en el binario como texto. La clave es una constante dentro del código.

## Vulnerabilidad

**XOR de un byte con clave hardcodeada** — el binario no está stripped; los símbolos `xor_key`, `decode_message` y `signal_bytes` guían el análisis directamente. La clave está en `xor_key` como un inmediato, no como string.

## Solución

### 1. Encontrar la clave en `xor_key`

```bash
objdump -d -M intel alien | grep -A10 '<xor_key>'
```

```asm
xor_key:
    mov BYTE PTR [rbp-0x1], 0x5c   ; ← clave XOR = 0x5c
    movzx eax, BYTE PTR [rbp-0x1]
    ret
```

**Clave = `0x5c`**

### 2. Volcar `signal_bytes` y descifrar

```bash
# Extraer los 17 bytes de .rodata (sección signal_bytes)
objdump -s -j .rodata alien | grep '2010'
```

```python
enc = bytes([0x08, 0x14, 0x27, 0x0f, 0x6d,
             0x3b, 0x32, 0x68, 0x30, 0x03,
             0x3a, 0x6c, 0x29, 0x32, 0x38,
             0x7d, 0x21])
key = 0x5c
flag = ''.join(chr(b ^ key) for b in enc)
print(flag)
```

> 🚩 **Flag:** omitida intencionalmente. Seguí los pasos para obtenerla.

## Takeaways

- Binarios no stripped: `nm` y los nombres de símbolos revelan la arquitectura del programa al instante.
- XOR de 1 byte: buscar `mov BYTE PTR [rbp-N], 0xNN` en la función de clave, extraer el inmediato.
- Rango de búsqueda en `.rodata`: `objdump -s -j .rodata` muestra todos los datos de solo lectura.

---
*Tropical Hunters CTF — Writeup por [Fabián Bustamante](https://github.com/fbustamante55)*
