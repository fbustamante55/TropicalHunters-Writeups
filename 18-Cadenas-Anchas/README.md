# Cadenas Anchas

| | |
|---|---|
| **Categoría** | Reversing |
| **Dificultad** | Fácil |
| **Puntos** | 100 |
| **Reto #** | 18 |

## Descripción

Un binario ELF que "esconde su texto en cadenas de dos bytes". El comando `strings` convencional no muestra nada útil, pero la flag está embebida en formato UTF-16LE (wide strings).

## Análisis

Los ejecutables compilados con soporte Unicode almacenan caracteres en **UTF-16LE**: cada carácter ocupa 2 bytes, con un byte nulo intercalado. `strings` por defecto lee strings de 1 byte e ignora por completo estas cadenas.

```
T\x00H\x00{\x00l\x00a\x00s\x00_\x00...
```

## Solución

```bash
# -e l = little-endian 16-bit (UTF-16LE)
strings -n 5 -e l cadenas-anchas
```

La flag aparece directamente.

**Alternativa con Python:**

```python
data = open('cadenas-anchas', 'rb').read()
texto = data.decode('utf-16-le', errors='ignore')
for tok in texto.split('\x00'):
    if 'TH{' in tok:
        print(tok)
```

> 🚩 **Flag:** omitida intencionalmente. Seguí los pasos para obtenerla.

## Takeaways

- `strings -e l` extrae wide strings UTF-16LE; `-e b` para big-endian; `-e S` para 32-bit LE.
- Binarios compilados con MSVC o MinGW suelen tener literales Unicode en wide strings.
- Cuando `strings` no muestra nada útil, siempre probar con `-e l`.

---
*Tropical Hunters CTF — Writeup por [Fabián Bustamante](https://github.com/fbustamante55)*
