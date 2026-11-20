# Wheel Spin

| | |
|---|---|
| **Categoría** | Crypto |
| **Dificultad** | Fácil |
| **Puntos** | 50 |
| **Reto #** | 37 |

## Descripción

`note.txt` contiene texto cifrado con letras desplazadas. La pista: *"solo hay 25 giros posibles."* → Cifrado César con desplazamiento desconocido.

## Vulnerabilidad

**Cifrado César — 25 posibilidades** — el cifrado más antiguo del mundo; fuerza bruta en microsegundos. El prefijo conocido `TH{` identifica el desplazamiento correcto instantáneamente.

## Solución

```python
cipher = "Rxvek, kyv fgvirkzfe zj r xf. Kyv rttvjj tfuv pfl evvu zj KY{25_jg1ej_4eu_p0l_n1e}. Slie kyzj efkv rwkvi ivruzex."

def caesar(text, shift):
    result = []
    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            result.append(chr((ord(ch) - base + shift) % 26 + base))
        else:
            result.append(ch)
    return ''.join(result)

for shift in range(1, 26):
    plain = caesar(cipher, shift)
    if "TH{" in plain:
        print(f"[+] Desplazamiento +{shift}: {plain}")
        break
```

**Atajo con known plaintext:** `desplazamiento = (ord('R') - ord('A') - (ord('A') - ord('A') + desplazamiento)) mod 26` → si `K → T`, `ord('T') - ord('K') = 9`.

> 🚩 **Flag:** omitida intencionalmente. Seguí los pasos para obtenerla.

## Takeaways

- César es completamente inseguro: 25 intentos determinan la clave.
- Known plaintext: si se conoce el prefijo del texto plano, el desplazamiento se calcula en una resta.
- CyberChef → "ROT13 Brute Force" automatiza el proceso con análisis de frecuencias.

---
*Tropical Hunters CTF — Writeup por [Fabián Bustamante](https://github.com/fbustamante55)*
