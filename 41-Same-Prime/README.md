# Same Prime

| | |
|---|---|
| **Categoría** | Crypto / RSA |
| **Dificultad** | Media |
| **Puntos** | 100 |
| **Reto #** | 41 |

## Descripción

`output.txt` contiene un RSA de 1024 bits. La pista: *"El generador de primos tenía un bug. Si al factorizar n solo sale un primo, no es coincidencia."*

## Vulnerabilidad

**RSA con p = q (módulo cuadrado perfecto)** — el generador de primos usó el mismo primo dos veces: `n = p²`. Factorizar un cuadrado perfecto es trivial: `p = isqrt(n)`. Con `p`, se calcula `φ(n) = p(p-1)` y se recupera la clave privada.

## Análisis

RSA normal: `n = p·q` → `φ(n) = (p-1)(q-1)`

Este caso: `n = p²` → `φ(n) = p(p-1)` → `d = e⁻¹ mod φ(n)`

## Solución

```python
import math
from Crypto.Util.number import long_to_bytes

n = 151874940357692155989377327353318766662973022353842468649472145511245667271377230457521799485394437743430419136036570217675533184557636140022982163061239952886070226042482259358163575786384269285644946145115470846597834777420609931099309725717855412673149972916834384245330335264729637748848716588147010803809
e = 65537
c = 151710478588850042300542837453296126195982880217021915874770405574517507523462008096486983321418851332878878648660580972539211589370204365990263947610210333678056987860767144377695183756914697348370553865150540366940992280854716801088845187815115909421845512067366204083854545254013853333029297397545032410690

p = math.isqrt(n)
assert p * p == n, "n no es un cuadrado perfecto"

phi = p * (p - 1)
d   = pow(e, -1, phi)
m   = pow(c, d, n)
print(long_to_bytes(m).decode())
```

> 🚩 **Flag:** omitida intencionalmente. Seguí los pasos para obtenerla.

## Takeaways

- `math.isqrt(n)` hace raíz cuadrada entera exacta en Python; verificar con `p*p == n`.
- `n = p²` es detectable con `sympy.factorint(n)` que devuelve `{p: 2}`.
- Generadores de números primos con estado compartido o seeding débil pueden producir `p = q`.

---
*Tropical Hunters CTF — Writeup por [Fabián Bustamante](https://github.com/fbustamante55)*
