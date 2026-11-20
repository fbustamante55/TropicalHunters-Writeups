# Uno por Uno (Reversing, 100 pts, 1 solve)

**Flag:** `TH{REDACTED}`

## Enunciado
Una "bóveda" digital (`boveda`, ELF de 64 bits para Linux) pide una clave y solo responde `Correcto` o `Incorrecto`. Nota del técnico: "la bóveda no guarda la clave entera en ningún lado; la revisa pieza por pieza". La clave tiene el formato `TH{...}` y es la flag. No hace falta ejecutar el programa.

## Solución
1. `file boveda` → ELF x86-64 estático, no stripped (parece compilado con Zig, con musl). Las funciones relevantes son `main` y `verificar`; el resto es libc.
2. `main` toma la clave de `argv[1]` o de `fgets`, y llama a `verificar` (0x10126f0). Si devuelve distinto de 0 imprime `Correcto`.
3. `verificar`:
   - `strlen(s) == 0x28` (40 caracteres).
   - Luego hay 40 comprobaciones independientes del estilo `movsx eax, BYTE PTR [rax+OFF]; cmp eax, VALOR`, escritas en **orden desordenado** de posiciones (por eso no se ve la cadena entera): cada una exige que `s[OFF] == VALOR`.
4. Extraer los pares (offset, valor) con un script sobre el desensamblado de `verificar` (`objdump -d -M intel`):
   ```python
   m = re.search(r'movsx\s+eax,BYTE PTR \[rax(?:\+0x([0-9a-f]+))?\]', l)   # offset (sin sufijo = 0)
   c = re.search(r'cmp\s+eax,0x([0-9a-f]+)', siguiente_linea)              # valor
   ```
   Salen exactamente los offsets 0..39, uno por uno. Ordenar por offset y convertir a ASCII:
   `TH{REDACTED}`

## Lecciones / técnica
- Verificación carácter a carácter con comparaciones inmediatas: cada byte aparece como constante en el código, así que la clave se reconstruye estáticamente.
- El desorden de las comparaciones solo estorba al leer a ojo; automatizar la extracción de pares (offset, valor) lo resuelve.
- Ojo: el offset 0 no lleva sufijo (`[rax]`), hay que contemplarlo en la regex.
- Se resolvió sin ejecutar el binario.
