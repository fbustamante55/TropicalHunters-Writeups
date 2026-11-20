# Tree

| | |
|---|---|
| **Categoría** | Reversing |
| **Dificultad** | Media |
| **Puntos** | 250 |
| **Reto #** | 33 |

## Descripción

Cuatro subrutinas (`stage1`–`stage4`) imprimen cada una un fragmento de la flag, pero `main` nunca las llama (condición `argc > 9999`). Cada stage descifra su fragmento con XOR `0x5a` y requiere valores de registro específicos para no abortar.

## Vulnerabilidad

**Código muerto alcanzable solo con depurador** — las stages existen y están completamente implementadas, pero la condición de llamada es inalcanzable en uso normal. Desde GDB se llaman directamente con los registros correctos.

## Análisis

| Función | Chequeo | Fuente cifrada |
|---------|---------|----------------|
| `stage1()` | ninguno | `enc.3` (5 bytes) |
| `stage2(edi)` | `edi == 0x1337` | `enc.2` (5 bytes) |
| `stage3(edi)` | `edi == 0xbeef` | `enc.1` (5 bytes) |
| `stage4(edi, esi)` | `edi == 0xa` y `esi == 0xb` | `enc.0` (4 bytes) |

`emit(ptr, len)`: `putchar(byte ^ 0x5a)` para cada byte.

## Solución

### Opción A — GDB

```bash
gdb ./tree
(gdb) b main
(gdb) r
(gdb) call stage1()
(gdb) set $edi = 0x1337
(gdb) call stage2($edi)
(gdb) set $edi = 0xbeef
(gdb) call stage3($edi)
(gdb) set $edi = 0xa
(gdb) set $esi = 0xb
(gdb) call stage4($edi, $esi)
```

### Opción B — Estático (Python)

```python
import struct

# Extraer enc.0–enc.3 de .rodata con objdump -s -j .rodata tree
enc = {
    3: bytes([...]),  # 5 bytes para stage1
    2: bytes([...]),  # 5 bytes para stage2
    1: bytes([...]),  # 5 bytes para stage3
    0: bytes([...]),  # 4 bytes para stage4
}
key = 0x5a
flag = ''.join(chr(b ^ key) for i in [3, 2, 1, 0] for b in enc[i])
print(flag)
```

> 🚩 **Flag:** omitida intencionalmente. Seguí los pasos para obtenerla.

## Takeaways

- Código inalcanzable en runtime es completamente analizable estáticamente.
- GDB `call func()` permite ejecutar funciones arbitrarias con registros controlados.
- Buscar `cmp argc, 0x270f` (9999) es un patrón clásico de "flag gate" en retos de reversing.

---
*Tropical Hunters CTF — Writeup por [Fabián Bustamante](https://github.com/fbustamante55)*
