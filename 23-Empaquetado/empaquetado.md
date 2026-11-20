# Empaquetado (Reversing, 100 pts, 1 solve)

**Código de acceso:** `1414213562373095048`
**Flag:** `TH{REDACTED}`

## Enunciado
Ejecutable Linux `empaquetado` en un servidor de respaldos: pide un código de acceso numérico y si es incorrecto responde `Código incorrecto`. `strings` casi no muestra nada legible. Hay que averiguar el código y obtener el secreto que muestra.

## Solución
1. `file` → ELF x86-64 estático, **sin section headers**; `strings` muestra `UPX!` y `$Info: This file is packed with the UPX executable packer`. Está empaquetado con UPX (por eso "parece vacío por dentro").
2. `upx -d` no estaba disponible (sin red), así que se desempaquetó en memoria: con gdb, `catch syscall read` + `run`, y al parar en el primer `read` (el programa ya está descomprimido y esperando entrada) se vuelca la memoria (`info proc mappings` + `dump binary memory`) de los tres segmentos (0x1000000-0x1013000, 0x1013000-0x1047000, 0x1047000-0x1052000). Con `objdump -D -b binary -m i386:x86-64 -M intel --adjust-vma=0x1013000` se desensambla.
3. En `main` (0x1013710): imprime `Introduce el código de acceso: `, lee con `fgets`, quita el salto de línea, convierte con `strtoul` base 10 (primer carácter debe ser dígito y no deben sobrar caracteres) y llama a `check(n)` (0x1013640):
   ```
   n*7 + 0x539 == 0x89621231f0843af1     (aritmética de 64 bits)
   ```
   Si es correcto llama a `reveal(n)` (0x1013670); si no, `Código incorrecto`.
4. Resolver la ecuación mod 2^64 (7 es impar, invertible):
   ```python
   n = ((0x89621231f0843af1 - 0x539) * pow(7, -1, 1<<64)) % (1<<64)
   # n = 1414213562373095048 (0x13a04bbdfdc9be88)
   ```
5. `reveal(n)`: para i en 0..40, `out[i] = TABLA[i] ^ ((n >> ((i & 7)*8)) & 0xff)`, con `TABLA` = 41 bytes en 0x1047a80 (`dcf6b291d238ff63fad1ae8fdc26c160d7caa890df22c57dd7cdaca2de24cd63fad7a498d3149922f5`). Luego imprime `Acceso concedido: %s`.
6. Aplicando la clave (los bytes de n) a TABLA sale la flag.

## Lecciones / técnica
- Binario UPX con section headers eliminados: sin `upx` se puede volcar la imagen ya descomprimida desde gdb, parando en el primer syscall `read`.
- Ecuación lineal modular `n*7+c == k` (mod 2^64): se invierte con el inverso multiplicativo de 7.
- El código de acceso es además la clave de un XOR cíclico de 8 bytes sobre el secreto.
- Nota: el binario se ejecutó dentro de gdb con stdin en /dev/null solo hasta el primer `read`, para volcarlo.
