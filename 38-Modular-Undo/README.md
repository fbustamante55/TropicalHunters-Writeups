# Modular Undo

| | |
|---|---|
| **Categoría** | Crypto |
| **Dificultad** | Fácil-Media |
| **Puntos** | 100 |
| **Reto #** | 38 |

## Descripción

`values.txt` contiene `p`, `a`, `b`, `c` de la ecuación `c ≡ a·secret + b (mod p)`. La solución es despejar `secret`.

## Vulnerabilidad

**Congruencia lineal modular sin secreto real** — como `p` es primo, el inverso multiplicativo de `a` existe y se calcula en O(log p). No hay clave secreta que romper; es matemática directa.

## Análisis

```
c ≡ a·secret + b (mod p)
a·secret ≡ c - b (mod p)
secret = (c - b) · a⁻¹ mod p
```

Como `p` es primo, `a⁻¹ mod p = pow(a, p-2, p)` (Fermat) o `pow(a, -1, p)` (Python 3.8+).

## Solución

```python
p = 23420514844235538247115893032913303930150123222328480875426664309848435335705858839309261542084794354203557552891799
a = 5603934371948044038320917624339114386282524030208721301338608365256958908915115857441879076803234273135634965578324
b = 2753013376414974076738280793482812000175255456077957235999318260089983522305363956579021642610838346954780220481155
c = 12154242000935093243878214189885972876555001032228277156705325100702179075516237227452661863056790524839385049821216

secret = (c - b) * pow(a, -1, p) % p
print(secret.to_bytes((secret.bit_length() + 7) // 8, 'big').decode())
```

> 🚩 **Flag:** omitida intencionalmente. Seguí los pasos para obtenerla.

## Takeaways

- Despejar `x` en `c ≡ ax + b (mod p)` requiere el inverso modular de `a`, no una clave privada.
- Python 3.8+: `pow(a, -1, p)` calcula el inverso modular directamente; alternativa: Algoritmo Extendido de Euclides.
- Una congruencia lineal sobre enteros modulo primo tiene solución única cuando `gcd(a, p) = 1`.

---
*Tropical Hunters CTF — Writeup por [Fabián Bustamante](https://github.com/fbustamante55)*
