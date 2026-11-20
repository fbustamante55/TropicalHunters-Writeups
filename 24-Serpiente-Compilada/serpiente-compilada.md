# Serpiente Compilada (Reversing/Python, 100 pts, 1 solve)

**Flag:** `TH{REDACTED}`

## Enunciado
Verificador de contraseñas en Python 3.12 del que solo queda `serpiente.pyc`; un colega dejó el desensamblado en `serpiente_dis.txt`. El programa responde "Correcto" solo con la contraseña buena, que es la flag.

## Solución
1. Del desensamblado (`dis`) del módulo: `CIFRADO` es una tupla de 33 enteros.
2. `verificar(clave)`:
   - Si `len(clave) != len(CIFRADO)` → `False`.
   - Si no: `all(...)` sobre un generador sobre `enumerate(clave)`.
3. El generador (`<genexpr>`) evalúa para cada `(i, c)`:
   ```
   ord(c) ^ ((i*7 + 3) & 255) == CIFRADO[i]
   ```
   Orden de operaciones en el bytecode: `i*7`, `+3`, `&255`, y entonces XOR con `ord(c)`.
4. `main` lee con `input('Contraseña: ').strip()` y llama a `verificar`.
5. Como XOR es reversible: `clave[i] = chr(CIFRADO[i] ^ ((i*7+3) & 255))`:
   ```python
   ''.join(chr(c ^ ((i*7+3) & 255)) for i, c in enumerate(CIFRADO))
   ```
   → `TH{REDACTED}` (33 caracteres, verificado contra la condición original).

## Lecciones / técnica
- Leer bytecode de CPython 3.12: `BINARY_OP` 5 = `*`, 0 = `+`, 1 = `&`, 12 = `^`; `COMPARE_OP` 40 = `==`.
- XOR con una keystream que depende solo de la posición es trivialmente invertible.
- No hizo falta decompilar el `.pyc` ni ejecutarlo.
