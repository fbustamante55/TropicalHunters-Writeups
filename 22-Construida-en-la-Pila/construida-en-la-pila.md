# Construida en la Pila (Reversing, 100 pts, 1 solve)

**Flag:** `TH{REDACTED}`

## Enunciado
`verificador` (ELF Linux) pide una contraseña y solo responde `Correcto` o `Incorrecto`. `strings` no encuentra nada útil. La contraseña es la flag; basta con leer `main`.

## Solución
1. `file` → ELF x86-64 estático, no stripped. Todo está en `main` (0x10135d0).
2. Al inicio de `main` hay 34 instrucciones `mov BYTE PTR [rbp-0x30+i], imm8` (de `rbp-0x30` a `rbp-0xf`) que construyen un buffer en la pila (stack string). Los bytes (`c9 d5 e6 f8 f1 ...`) no son ASCII legible, por eso `strings` no ve nada.
3. El programa lee la entrada con `fgets` (quita el `\n` con `strcspn`), y luego recorre los 34 (0x22) bytes del buffer haciendo `buf[i] ^= 0x9d`.
4. Compara: `strlen(entrada) == 0x22` y `entrada[i] == buf[i]` para los 34 bytes; imprime `Correcto` o `Incorrecto`.
5. Extraer los 34 bytes, hacer XOR con `0x9d` y decodificar: `TH{REDACTED}`.

## Lecciones / técnica
- Stack strings + XOR de un solo byte: el texto se arma en tiempo de ejecución y se compara contra la entrada, así que la contraseña está en el binario aunque `strings` no la encuentre.
- Al extraer con regex, cuidado con los límites de offsets (el último byte está en `rbp-0xf`).
- Se resolvió estáticamente, sin ejecutar el binario.
