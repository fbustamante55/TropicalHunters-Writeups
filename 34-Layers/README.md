# Layers

| | |
|---|---|
| **Categoría** | Crypto |
| **Dificultad** | Fácil |
| **Puntos** | 50 |
| **Reto #** | 34 |

## Descripción

`note.txt` contiene una cadena que parece Base64. La pista: *"No hay ninguna llave. Solo capas. Codificar no es cifrar."* Tres capas de codificación anidadas.

## Vulnerabilidad

**Triple codificación sin cifrado real** — Base64 → Hexadecimal → Base32. Ninguna capa usa clave; todas son completamente reversibles por cualquiera.

## Análisis

| Capa | Señal | Codificación |
|------|-------|--------------|
| 1 (exterior) | Mayúsculas + minúsculas + números | Base64 |
| 2 (medio) | Solo `0-9` y `a-f` | Hexadecimal |
| 3 (interior) | Solo `A-Z` y `2-7`, padding `======` | Base32 |

## Solución

```python
import base64

s = "NGI1MjQ1NDg1NzM1NDQ0OTRmNDk1YTU0NDc1ODMzNGQ0NzUyMzQ1NDQ3MzQ1NDU0NGMzNTM1NDQ0NzM0NTI1MTRjMzU1NjU0NDczNjRjNTQ1MDU1M2QzZDNkM2QzZDNk"

step1 = base64.b64decode(s).decode()          # Base64 → hex string
step2 = bytes.fromhex(step1).decode()          # hex → Base32 string
flag  = base64.b32decode(step2).decode()       # Base32 → plaintext
print(flag)
```

> 🚩 **Flag:** omitida intencionalmente. Seguí los pasos para obtenerla.

## Takeaways

- Identificar codificaciones por su alfabeto: `[A-Za-z0-9+/]` = Base64; `[0-9a-f]` = Hex; `[A-Z2-7]` = Base32.
- Codificar ≠ cifrar: sin clave, cualquier codificación es reversible con una sola instrucción Python.
- CyberChef ("Magic" mode) detecta automáticamente capas de codificación comunes.

---
*Tropical Hunters CTF — Writeup por [Fabián Bustamante](https://github.com/fbustamante55)*
