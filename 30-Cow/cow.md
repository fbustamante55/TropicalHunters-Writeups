# Cow (Reversing, 200 pts, 1 solve)

**Flag:** `TH{REDACTED}`

## Enunciado
Una vaca pide una clave. El validador comprueba un sistema de restricciones (sumas, diferencias, XOR) sobre los bytes de la entrada; solo una cadena las cumple. Se sugiere Z3.

## Solución
1. `file cow` → ELF x86-64 PIE, no stripped. Funciones: `check`, `cow`, `clear_screen`, `main`.
2. Desensamblar `check` (`objdump -d -M intel`). Restricciones sobre la entrada `s`:
   - `strlen(s) == 18`
   - `memcmp(s, "TH{", 3) == 0` (prefijo en .rodata 0x2020)
   - `s[17] == '}'`
   - Sea `p = s+3` (14 bytes, `p[0..13]`): todos imprimibles (0x21 a 0x7e).
   - `sum(p[0..13]) == 0x4dc` (1244)
   - `p[i+1] - p[i] == D[i]` para i = 0..12, con `D` (13 enteros de 32 bits en .rodata 0x20a0) = `[-71, 44, 13, -60, 47, 19, -63, 64, 2, -66, 57, 10, -67]`
   - `p[0] ^ p[2] == 0x25`
   - `p[3] ^ p[5] == 0x33`
3. Resolución: como las diferencias fijan toda la cadena a partir de `p[0]`, basta iterar `p[0]` en 0x21..0x7e, reconstruir `p` y filtrar por suma y XORs (no hizo falta Z3; no estaba instalado). Una única solución:
   `TH{REDACTED}`

## Lecciones / técnica
- Reversing estático de un validador por restricciones; extraer constantes de .rodata (`D.0`) y traducirlas a ecuaciones.
- Con restricciones de diferencias consecutivas el espacio es de 1 variable libre: fuerza bruta equivale a un solver.
- Nota: la flag se obtuvo de forma estática; no se ejecutó el binario.
