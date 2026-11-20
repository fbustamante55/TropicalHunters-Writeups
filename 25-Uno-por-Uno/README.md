# Uno por Uno

| | |
|---|---|
| **Categoría** | Reversing |
| **Dificultad** | Fácil |
| **Puntos** | 100 |
| **Reto #** | 25 |

## Descripción

Una "bóveda" digital (`boveda`, ELF x86-64) pide una clave y solo responde `Correcto` o `Incorrecto`. La clave tiene exactamente 40 caracteres y se verifica carácter por carácter en orden desordenado.

## Vulnerabilidad

**Verificación carácter a carácter con inmediatos hardcodeados** — cada `cmp eax, VALOR` compara un byte de la entrada con un valor literal en el ejecutable. El desensamblado expone todos los pares `(offset, valor)` directamente.

## Solución

### 1. Reconocimiento

```bash
file boveda    # ELF x86-64 estático, no stripped (compilado con Zig/musl)
objdump -d -M intel boveda | grep 'cmp' | grep -E 'eax,0x'
```

### 2. Extraer los pares (offset, valor)

El offset 0 aparece como `[rax]` (sin desplazamiento); los demás como `[rax+0xNN]`.

```bash
objdump -d -M intel boveda \
  | grep -E '\[rax(\+0x[0-9a-f]+)?\]' -A1 \
  | grep 'cmp.*eax,0x'
```

### 3. Reconstruir la clave

```python
# Pares extraídos del objdump — (offset_hex, valor_hex)
pares = [
    (0x00, 0x54), (0x01, 0x48), (0x02, 0x7b),
    # ... (40 pares en total, en orden desordenado)
]
pares.sort(key=lambda x: x[0])
flag = ''.join(chr(v) for _, v in pares)
print(flag)
```

> 🚩 **Flag:** omitida intencionalmente. Seguí los pasos para obtenerla.

## Takeaways

- Verificación carácter a carácter: reconstruir directamente del desensamblado, sin ejecutar.
- El desorden de los `cmp` solo estorba al leerlo a ojo; ordenar por offset lo resuelve en segundos.
- Binarios Zig/musl tienen mucho código de runtime extra — buscar la función `main` o `verificar` por sus símbolos.

---
*Tropical Hunters CTF — Writeup por [Fabián Bustamante](https://github.com/fbustamante55)*
