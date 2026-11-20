# Empaquetado

| | |
|---|---|
| **Categoría** | Reversing |
| **Dificultad** | Media |
| **Puntos** | 100 |
| **Reto #** | 23 |
| **Código de acceso** | `1414213562373095048` |

## Descripción

Ejecutable Linux `empaquetado`: solicita un código de acceso numérico. `strings` casi no muestra nada. Hay que determinar el código para obtener el secreto.

## Vulnerabilidad

**UPX packer** — el binario está comprimido; `strings` no encuentra contenido útil porque los datos están en el payload comprimido. Se desempaqueta volcando la memoria desde GDB.

## Solución

### 1. Detectar el packer

```bash
strings empaquetado | grep UPX
# $Info: This file is packed with the UPX executable packer
```

### 2. Volcar la memoria en GDB

```bash
gdb ./empaquetado
(gdb) catch syscall read
(gdb) run
# Pausa en el primer read()
(gdb) info proc mappings
(gdb) dump binary memory dump.bin 0x1000000 0x1052000
```

### 3. Desensamblar el volcado

```bash
objdump -D -b binary -m i386:x86-64 -M intel \
  --adjust-vma=0x1013000 dump.bin | grep -A30 'main'
```

### 4. Entender la verificación

La función `check(n)` verifica que `n == floor(sqrt(2)) * 10^18` (los primeros 19 dígitos de √2):

```python
import math
print(math.isqrt(2 * 10**36))   # 1414213562373095048
```

```bash
echo "1414213562373095048" | ./empaquetado
```

> 🚩 **Flag:** omitida intencionalmente. Seguí los pasos para obtenerla.

## Takeaways

- Detectar packers: `strings | grep -i 'upx\|packer'` o `die`/`exeinfo`.
- Sin `upx -d` disponible, GDB + dump de memoria es el método universal.
- `math.isqrt` en Python hace raíz cuadrada entera exacta, útil para identificar constantes matemáticas.

---
*Tropical Hunters CTF — Writeup por [Fabián Bustamante](https://github.com/fbustamante55)*
