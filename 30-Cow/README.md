# Cow

| | |
|---|---|
| **Categoría** | Reversing |
| **Dificultad** | Media |
| **Puntos** | 200 |
| **Reto #** | 30 |

## Descripción

Una vaca pide una clave de 18 caracteres. El validador comprueba un sistema de restricciones sobre los bytes de la entrada: longitud, prefijo `TH{`, sufijo `}`, rango imprimible, suma total, diferencias consecutivas y dos XOR.

## Vulnerabilidad

**Sistema de restricciones lineales** — las diferencias consecutivas entre caracteres están hardcodeadas en `.rodata`, lo que permite reconstruir toda la cadena iterando solo el primer byte.

## Solución

```python
# Diferencias extraídas de .rodata (13 valores para 14 bytes del "payload")
D = [-71, 44, 13, -60, 47, 19, -63, 64, 2, -66, 57, 10, -67]
# Suma total del payload: 0x4dc = 1244
# XOR: p[0] ^ p[2] == 0x25,  p[3] ^ p[5] == 0x33
# Rango imprimible: 0x21 <= p[i] <= 0x7e

for start in range(0x21, 0x7f):
    p = [start]
    for d in D:
        p.append(p[-1] + d)
    if any(c < 0x21 or c > 0x7e for c in p):
        continue
    if sum(p) != 0x4dc:
        continue
    if (p[0] ^ p[2]) != 0x25:
        continue
    if (p[3] ^ p[5]) != 0x33:
        continue
    flag = "TH{" + ''.join(chr(c) for c in p) + "}"
    print(flag)
    break
```

> 🚩 **Flag:** omitida intencionalmente. Seguí los pasos para obtenerla.

## Takeaways

- Diferencias consecutivas hardcodeadas + un solo grado de libertad = búsqueda lineal de 94 candidatos.
- Z3 Theorem Prover automatiza este tipo de restricciones cuando hay más variables: `Solver().add(...)`.
- El nombre del reto ("Cow" / Z3) es una pista directa sobre la herramienta esperada.

---
*Tropical Hunters CTF — Writeup por [Fabián Bustamante](https://github.com/fbustamante55)*
