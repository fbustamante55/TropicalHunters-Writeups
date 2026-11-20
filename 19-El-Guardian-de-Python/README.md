# El Guardián de Python

| | |
|---|---|
| **Categoría** | Reversing |
| **Dificultad** | Fácil |
| **Puntos** | 50 |
| **Reto #** | 19 |

## Descripción

Un guardián escrito en Python pide una contraseña. El código fuente está a la vista y el autor afirma que "la contraseña no está escrita ahí". La transformación usada es reversible.

## Análisis

```python
def preparar(intento):
    volteado = intento[::-1]
    return base64.b64encode(volteado.encode()).decode()

SECRETO = "fTcyX2F0cmV1cF9hbF9lcmJhX29naWRvY19sZV9yZWVse0hU"
```

`preparar(intento)` = `base64(reverse(intento))`. La inversa es:

```
reverse(base64_decode(SECRETO))
```

## Solución

```python
import base64

SECRETO = "fTcyX2F0cmV1cF9hbF9lcmJhX29naWRvY19sZV9yZWVse0hU"
flag = base64.b64decode(SECRETO).decode()[::-1]
print(flag)
```

> 🚩 **Flag:** omitida intencionalmente. Seguí los pasos para obtenerla.

## Takeaways

- Base64 + reverse no es protección: cualquier transformación invertible expone el secreto con análisis estático.
- Una contraseña real se compara contra un hash lento con sal: **bcrypt**, **Argon2id** o **scrypt**.

---
*Tropical Hunters CTF — Writeup por [Fabián Bustamante](https://github.com/fbustamante55)*
