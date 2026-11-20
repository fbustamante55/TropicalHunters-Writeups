# Short Message

| | |
|---|---|
| **Categoría** | Crypto / RSA |
| **Dificultad** | Media |
| **Puntos** | 200 |
| **Reto #** | 42 |

## Descripción

`output.txt` contiene un RSA con `e = 3` y módulo de 2048 bits. La pista: *"El módulo es grande, pero el mensaje no."*

## Vulnerabilidad

**Raíz e-ésima entera (cube root attack)** — con `e = 3` y mensaje corto sin padding, `m³ < n`, por lo que el cifrado es `c = m³` sin reducción modular. La flag se recupera calculando `∛c` como entero puro.

## Análisis

Cifrado RSA: `c = m^e mod n`. Si `m^3 < n` → `c = m^3` exacto (sin mod). El módulo de 2048 bits es irrelevante: no importa su tamaño cuando `m` es corto.

## Solución

```python
def icbrt(x):
    # Raíz cúbica entera exacta por búsqueda binaria
    lo, hi = 0, 1 << ((x.bit_length() // 3) + 2)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if mid**3 <= x:
            lo = mid
        else:
            hi = mid - 1
    return lo

c = 2484387996737433984301073817614508984426831418824775599032079868027870212259289463440685647314848665461680420046952130233609112698853430165003618760033339134027178043600133948017084115557

m = icbrt(c)
assert m**3 == c, "c no es un cubo perfecto exacto"
print(m.to_bytes((m.bit_length() + 7) // 8, "big").decode())
```

> 🚩 **Flag:** omitida intencionalmente. Seguí los pasos para obtenerla.

## Takeaways

- RSA con `e = 3` sin padding OAEP/PKCS#1 es vulnerable a múltiples ataques (cube root, Håstad broadcast).
- El tamaño de `n` no protege si `m^e < n`: el cifrado se convierte en aritmética entera pura.
- Siempre usar OAEP con RSA; nunca `e = 3` sin padding robusto.

---
*Tropical Hunters CTF — Writeup por [Fabián Bustamante](https://github.com/fbustamante55)*
