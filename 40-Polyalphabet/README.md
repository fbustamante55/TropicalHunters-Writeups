# Polyalphabet

| | |
|---|---|
| **Categoría** | Crypto |
| **Dificultad** | Fácil-Media |
| **Puntos** | 100 |
| **Reto #** | 40 |

## Descripción

`intercept.txt` contiene un reporte militar cifrado con Vigenère (clave de 6 letras que se repite). La secuencia `Lmi` aparece 3 veces y `vbcxjy` aparece 2 veces — índicio del largo de clave.

## Vulnerabilidad

**Cifrado Vigenère — Kasiski + known plaintext** — repeticiones de secuencias revelan la longitud de la clave; el encabezado típico de un reporte inglés permite recuperar los 6 bytes de la clave por XOR modular.

## Análisis

**Kasiski:** diferencias entre posiciones de `Lmi` son múltiplos de 6 → longitud = 6.

**Known plaintext** (inicio `FIELD REPORT FROM THE`):

| Pos mod 6 | Cifrado | Plano | Clave |
|-----------|---------|-------|-------|
| 0 | C (2) | F (5) | 23 → X |
| 1 | v (21) | I (8) | 13 → N |
| 2 | n (13) | E (4) | 9 → J |
| 3 | d (3) | L (11) | 18 → S |
| 4 | i (8) | D (3) | 5 → F |
| 5 | v (21) | R (17) | 4 → E |

**Clave:** `XNJSFE`

## Solución

```python
def vigenere_decrypt(ct, key):
    result = []
    ki = 0
    for ch in ct:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            k = ord(key[ki % len(key)].upper()) - ord('A')
            result.append(chr((ord(ch) - base - k) % 26 + base))
            ki += 1
        else:
            result.append(ch)
    return ''.join(result)

cipher = "Cvndi vbcxjy jobv lmi kbalmioa xmytlfc..."
key    = "XNJSFE"
print(vigenere_decrypt(cipher, key))
```

> 🚩 **Flag:** omitida intencionalmente. Seguí los pasos para obtenerla.

## Takeaways

- Vigenère: Kasiski → longitud de clave; Friedman → confirmación; known plaintext → recuperación directa.
- Repeticiones en el texto cifrado siempre revelan información sobre la clave en cifrados periódicos.
- Vigenère fue considerado "indescifrable" por ~300 años; se rompe con análisis de frecuencias en segundos hoy.

---
*Tropical Hunters CTF — Writeup por [Fabián Bustamante](https://github.com/fbustamante55)*
