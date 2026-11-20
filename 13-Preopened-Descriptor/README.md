# Preopened Descriptor

| | |
|---|---|
| **Categoría** | Pwn |
| **Dificultad** | Fácil |
| **Puntos** | 100 |
| **Reto #** | 13 |
| **Conexión** | `nc chals.tropicalhunters.com 9011` |

## Descripción

No es posible abrir archivos nuevos, pero el programa ya dejó uno con la flag abierto en un file descriptor específico. El objetivo es adivinar ese número.

## Análisis

```c
FILE *tmp = tmpfile();           // fd asignado por el OS
// copia flag.txt al tmp...
rewind(tmp);
dup2(fileno(tmp), 7);            // flag queda accesible en fd 7
fclose(tmp_original);

scanf("%d", &fd);                // acepta 3 ≤ fd ≤ 9
read(fd, buf, 0x3f);
fputs(buf, stdout);
```

`dup2(src, 7)` duplica el descriptor al **fd 7**, número fijo hard-codeado visible en el binario (`mov $0x7, %esi` antes de `call dup2`).

## Solución

```bash
echo 7 | nc chals.tropicalhunters.com 9011
```

> 🚩 **Flag:** omitida intencionalmente. Seguí los pasos para obtenerla.

## Takeaways

- `dup2(oldfd, newfd)` crea un alias del fd en un número fijo; ambos apuntan al mismo archivo.
- Buscar `dup2` en el desensamblado y leer el segundo argumento (`esi`) revela el fd destino inmediatamente.
- Los fd 0/1/2 son stdin/stdout/stderr; usar fd 7 no oculta realmente el descriptor.

---
*Tropical Hunters CTF — Writeup por [Fabián Bustamante](https://github.com/fbustamante55)*
