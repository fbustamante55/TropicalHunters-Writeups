# Mensaje hexadecimal

| | |
|---|---|
| **Categoría** | Forensics |
| **Dificultad** | Fácil |
| **Puntos** | 50 |
| **Reto #** | 46 |

## Descripción

Una nota encontrada en la Operación Eclipse tiene al pie un bloque de pares hexadecimales escritos a mano. La clave de acceso al expediente está codificada en hex.

## Solución

### 1. Identificar la codificación

Pares `[0-9a-f]{2}` separados por espacios → hexadecimal ASCII. Los bytes `54 48 7b` corresponden a `T`, `H`, `{` — prefijo de la flag visible incluso sin decoder.

### 2. Decodificar

```bash
xxd -r -p nota_hex.txt
```

**En Python:**

```python
datos = "4e6f7461...31367d"   # pegar sin espacios
print(bytes.fromhex(datos.replace(" ", "")).decode())
```

> 🚩 **Flag:** omitida intencionalmente. Seguí los pasos para obtenerla.

## Takeaways

- `xxd -r -p` convierte hex dump a bytes; `xxd` hace lo inverso.
- Pares `54 48` = `TH` → reconocible sin herramientas, útil para localizar la flag en un dump largo.
- Hex es representación, no cifrado: completamente reversible sin clave.

---
*Tropical Hunters CTF — Writeup por [Fabián Bustamante](https://github.com/fbustamante55)*
