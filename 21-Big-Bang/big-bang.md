# Big Bang (Reversing/Warmup, 50 pts, 1 solve)

**Flag:** `TH{REDACTED}`

## Enunciado
"Todo gran destino empieza con un solo punto. Ejecuta el binario y observa el big bang; el universo guarda un secreto dentro del propio ejecutable." Pista: dónde viven las cadenas de texto legibles en un binario.

## Solución
1. `file bigbang` → ELF x86-64 PIE, dinámico, no stripped.
2. `strings -n 4 bigbang | grep 'TH{'` devuelve directamente `TH{REDACTED}`. En la salida de `strings` aparecen también `El inicio de tu destino`, `\033[33m%c` y `\033[30m%s`: el programa anima caracteres en amarillo y luego imprime la flag con el código de color `30m` (negro), por lo que no se ve en un terminal oscuro aunque se imprima.
3. No fue necesario ejecutar el binario.

## Lecciones / técnica
- Primer paso en cualquier reto de reversing: `strings | grep 'TH{'`.
- Texto "invisible" en la animación = escape ANSI de color negro sobre fondo negro; el texto sigue en la salida y en el binario.
