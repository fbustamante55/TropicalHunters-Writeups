# Robot

| | |
|---|---|
| **Categoría** | Reversing |
| **Dificultad** | Fácil-Media |
| **Puntos** | 200 |
| **Reto #** | 28 |

## Descripción

El robot procesa la flag pero nunca la imprime. Está repartida en cuatro funciones (`part_a`–`part_d`), cada una con su fragmento cifrado con XOR y su propia clave de 1 byte. El programa solo anima un dibujo ASCII en un bucle infinito.

## Vulnerabilidad

**XOR de 1 byte repartido en 4 funciones** — el binario no está stripped; los símbolos `part_a`..`part_d`, `assemble_flag` y `enc.1`..`enc.4` hacen trivial seguir el flujo. La flag completa existe en memoria pero nunca llega a `printf`/`puts`.

## Solución

### 1. Mapear el flujo

```bash
nm robot | grep -E 'part_|assemble_flag|enc\.'
```

`assemble_flag` llama en orden: `part_a → part_b → part_c → part_d`, cada una escribe 4 bytes en su sección del buffer (16 bytes + null terminator).

### 2. Extraer clave y datos cifrados de cada `part_X`

```bash
objdump -d -M intel robot | grep -A30 '<part_a>'
objdump -s -j .rodata robot
```

| Función | Clave | Datos cifrados (`.rodata`) |
|---------|-------|---------------------------|
| `part_a` | `0x1f` | `enc.4` (4 bytes) |
| `part_b` | `0x2b` | `enc.3` (4 bytes) |
| `part_c` | `0x3c` | `enc.2` (4 bytes) |
| `part_d` | `0x4d` | `enc.1` (4 bytes) |

### 3. Descifrar

```python
parts = [
    ([0x6b, 0x77, 0x7c, 0x63], 0x1f),  # part_a
    ([0x1f, 0x65, 0x5f, 0x7a], 0x2b),  # part_b
    ([0x7c, 0x7e, 0x61, 0x64], 0x3c),  # part_c
    ([0x3f, 0x65, 0x0e, 0x7c], 0x4d),  # part_d
]
flag = ''.join(chr(b ^ k) for data, k in parts for b in data)
print(flag)
```

> 🚩 **Flag:** omitida intencionalmente. Seguí los pasos para obtenerla.

## Takeaways

- Dividir la flag en partes con claves distintas no aumenta la seguridad si cada parte es analizable por separado.
- `assemble_flag` con símbolos no stripped es un mapa del tesoro: revela el orden de ensamblado y los tamaños.
- Un programa que nunca imprime su resultado es un indicador claro de que el secreto se analiza estáticamente.

---
*Tropical Hunters CTF — Writeup por [Fabián Bustamante](https://github.com/fbustamante55)*
