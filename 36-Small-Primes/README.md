# Small Primes

| | |
|---|---|
| **Categoría** | Crypto / RSA |
| **Dificultad** | Fácil |
| **Puntos** | 50 |
| **Reto #** | 36 |

## Descripción

`output.txt` contiene `n`, `e`, `c` de un RSA. El módulo tiene solo 39 dígitos (~128 bits). La pista: *"RSA, pero alguien ahorró en el tamaño de los primos."*

## Vulnerabilidad

**RSA con módulo de 128 bits — factorizable en milisegundos** — un módulo seguro debe tener al menos 2048 bits (617 dígitos). Con 128 bits, `p` y `q` son de ~64 bits cada uno y se factorizan trivialmente con FactorDB o `sympy.factorint`.

## Solución

```python
from sympy import factorint
from Crypto.Util.number import long_to_bytes

n = 297692863915623136840407191535126629137
e = 65537
c = 93643100307851213487991252155561738250

# Factorizar n (< 1 s)
factors = factorint(n)
p, q = list(factors.keys())

# Calcular d
phi = (p - 1) * (q - 1)
d = pow(e, -1, phi)

# Descifrar
m = pow(c, d, n)
print(long_to_bytes(m).decode())
```

**Alternativa online:** FactorDB.com — buscar `n` directamente.

> 🚩 **Flag:** omitida intencionalmente. Seguí los pasos para obtenerla.

## Takeaways

- Tamaño de `n` define la seguridad RSA, no de `e`. Un módulo de 128 bits es equivalente a ninguna seguridad.
- FactorDB.com tiene pre-computadas factorizaciones de números pequeños; para CTF es el primer recurso.
- RSA seguro mínimo en 2025: módulos de 2048 bits; recomendado 4096 bits para datos con vida útil larga.

---
*Tropical Hunters CTF — Writeup por [Fabián Bustamante](https://github.com/fbustamante55)*
