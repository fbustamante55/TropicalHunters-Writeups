# Serpiente Compilada

| | |
|---|---|
| **Categoría** | Reversing |
| **Dificultad** | Fácil |
| **Puntos** | 100 |
| **Reto #** | 24 |

## Descripción

Verificador de contraseñas en Python 3.12 del que solo queda `serpiente.pyc`. Un archivo `serpiente_dis.txt` contiene el desensamblado del bytecode. La contraseña correcta es la flag.

## Vulnerabilidad

**Bytecode CPython reversible** — el bytecode `.pyc` contiene todas las constantes y la lógica de verificación legible con `dis`. El cifrado XOR posicional es trivialmente invertible.

## Análisis

Del desensamblado (opcodes CPython 3.12):

```python
CIFRADO = (...)   # tupla de 33 enteros

def verificar(clave):
    if len(clave) != len(CIFRADO):
        return False
    return all(
        ord(c) ^ ((i * 7 + 3) & 255) == CIFRADO[i]
        for i, c in enumerate(clave)
    )
```

Opcodes relevantes: `BINARY_OP 5` = `*`, `BINARY_OP 0` = `+`, `BINARY_OP 1` = `&`, `BINARY_OP 12` = `^`, `COMPARE_OP 40` = `==`.

## Solución

XOR es su propia inversa: si `ord(c) ^ K == V`, entonces `c = chr(V ^ K)`.

```python
# Extraer CIFRADO del .pyc con dis o del _dis.txt
import dis, marshal

with open('serpiente.pyc', 'rb') as f:
    f.read(16)   # magic + flags + timestamp + size
    code = marshal.loads(f.read())

dis.dis(code)   # muestra CIFRADO como LOAD_CONST

CIFRADO = (...)   # copiar la tupla del output de dis

flag = ''.join(
    chr(v ^ ((i * 7 + 3) & 255))
    for i, v in enumerate(CIFRADO)
)
print(flag)
```

> 🚩 **Flag:** omitida intencionalmente. Seguí los pasos para obtenerla.

## Takeaways

- El bytecode CPython es completamente legible: `python -m dis archivo.pyc` o `marshal.loads`.
- XOR con keystream posicional es invertible en una línea de Python.
- Un `.pyc` no protege el secreto — solo lo retrasa unos minutos.

---
*Tropical Hunters CTF — Writeup por [Fabián Bustamante](https://github.com/fbustamante55)*
