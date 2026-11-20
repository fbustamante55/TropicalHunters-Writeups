# Construida en la Pila

| | |
|---|---|
| **Categoría** | Reversing |
| **Dificultad** | Fácil |
| **Puntos** | 100 |
| **Reto #** | 22 |

## Descripción

`verificador` (ELF x86-64) pide una contraseña y solo responde `Correcto` o `Incorrecto`. `strings` no encuentra nada útil — el secreto se construye en tiempo de ejecución.

## Vulnerabilidad

**Stack strings + XOR de un byte** — el binario construye el texto byte a byte en la pila con instrucciones `mov BYTE PTR [rbp-N], imm8` y luego aplica XOR con `0x9d` antes de comparar. `strings` no detecta los bytes dispersos; `objdump` sí muestra los inmediatos.

## Solución

### 1. Reconocimiento

```bash
file verificador     # ELF x86-64 estático, no stripped
strings verificador  # nada útil
```

### 2. Localizar el stack string

```bash
objdump -d -M intel verificador | grep -A5 'main'
```

34 instrucciones `mov BYTE PTR [rbp-0x30+i], imm8` construyen el buffer. Los bytes en hex: `c9 d5 e6 f8 f1 ...`

### 3. Identificar la clave XOR

Más adelante en `main`:

```asm
; bucle: buf[i] ^= 0x9d  (34 iteraciones)
; luego: strcmp(buf, input)
```

### 4. Recuperar la flag

```python
raw = [0xc9, 0xd5, 0xe6, 0xf8, 0xf1,
       0xe4, 0xeb, 0xf8, 0xf0, 0xe1,
       0xf8, 0xe4, 0xe1, 0xf2, 0xed,
       0xf1, 0xed, 0xf0, 0xed, 0xe2,
       0xed, 0xf1, 0xe4, 0xf2, 0xe2,
       0xe2, 0xed, 0xe2, 0xf2, 0xed,
       0xf1, 0xe4, 0xf5, 0x0a]      # 34 bytes del stack string

flag = ''.join(chr(b ^ 0x9d) for b in raw)
print(flag)
```

> 🚩 **Flag:** omitida intencionalmente. Seguí los pasos para obtenerla.

## Takeaways

- Stack strings + XOR de 1 byte: `strings` no los ve, pero `objdump` muestra todos los inmediatos.
- Si `strings` no da la flag, busca `mov byte [rbp-x], imm` en el desensamblado de `main`.
- XOR es simétrico: si `b ^ 0x9d == result`, entonces `result ^ 0x9d == b`.

---
*Tropical Hunters CTF — Writeup por [Fabián Bustamante](https://github.com/fbustamante55)*
