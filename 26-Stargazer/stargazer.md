# Stargazer (Reversing, 100 pts, 1 solve)

**Flag:** `TH{REDACTED}`

## Enunciado
Un telescopio observa un cielo estrellado. La bandera está en texto claro dentro del binario, pero `strings` no la da; probablemente se construye en tiempo de ejecución. Abrirlo en un descompilador y leer `main`.

## Solución
1. `file s` → ELF x86-64 PIE, no stripped. Funciones: `main`, `clear_screen`, `draw_scene`.
2. En `main` (`objdump -d -M intel`), 23 instrucciones `mov BYTE PTR [rbp-0x20+i], imm8` construyen un buffer en la pila carácter por carácter (por eso `strings` no lo ve), terminado en 0x00:
   `54 48 7b .. .. .. 7d`
3. Se imprime con `puts` solo si `argc > 0x270f` (9999), condición que no se cumple normalmente; el resto de `main` es un bucle infinito que dibuja el cielo (`srand(time)`, `draw_scene`).
4. Decodificar los bytes → `TH{REDACTED}`. No hace falta ejecutar el binario.

## Lecciones / técnica
- Stack strings: texto construido byte a byte con `mov byte [rbp-x], imm` para evadir `strings`.
- Leer el desensamblado de `main` y convertir los inmediatos a ASCII.
