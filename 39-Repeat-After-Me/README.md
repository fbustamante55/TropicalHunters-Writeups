# Repeat After Me

| | |
|---|---|
| **Categoría** | Crypto |
| **Dificultad** | Fácil |
| **Puntos** | 100 |
| **Reto #** | 39 |

## Descripción

`ciphertext.txt` es un hex dump cifrado con XOR de llave repetida de varios bytes. La pista: *"Ya sabés cómo se ve una flag."*

## Vulnerabilidad

**XOR con clave repetida + known plaintext** — conocer el prefijo `TH{` y el sufijo `}` del texto plano permite recuperar la clave completa sin fuerza bruta.

## Análisis

```
key[i] = ciphertext[i] XOR plaintext[i]
```

| Pos | Cifrado | Plano | Clave |
|-----|---------|-------|-------|
| 0 | `0x25` | `T` (0x54) | `0x71` → `q` |
| 1 | `0x2e` | `H` (0x48) | `0x66` → `f` |
| 2 | `0x12` | `{` (0x7b) | `0x69` → `i` |
| 27 | `0x11` | `}` (0x7d) | `0x6c` → `l` |

Posición 27 mod 4 = 3 → cuarto byte de clave = `l`. **Clave:** `qfil`

## Solución

```python
ct = bytes.fromhex("252e12181955360045151d33131f1d5f2e0559191f121a3305565911")
key = b"qfil"
pt = bytes(c ^ key[i % len(key)] for i, c in enumerate(ct))
print(pt.decode())
```

> 🚩 **Flag:** omitida intencionalmente. Seguí los pasos para obtenerla.

## Takeaways

- XOR con clave repetida + prefijo conocido: recuperar la clave es una sola operación de XOR.
- La longitud de la clave se deduce del índice del último byte conocido (`len - 1) mod L = known_pos mod L`.
- Vigenère en XOR y cifrado Vernam son vulnerables al mismo ataque de known plaintext.

---
*Tropical Hunters CTF — Writeup por [Fabián Bustamante](https://github.com/fbustamante55)*
