# Stargazer

| | |
|---|---|
| **Categoría** | Reversing |
| **Dificultad** | Fácil |
| **Puntos** | 100 |
| **Reto #** | 26 |

## Descripción

Un telescopio observa un cielo estrellado. La flag está en el binario pero `strings` no la entrega — se construye en tiempo de ejecución. La condición para imprimirla requiere más de 9999 argumentos en la línea de comandos.

## Vulnerabilidad

**Stack string con condición de impresión imposible** — la flag se almacena byte a byte en la pila (`mov BYTE PTR [rbp-N], imm`), impidiéndole a `strings` detectarla. La condición `argc > 9999` hace que nunca se imprima al ejecutar el binario normalmente. El análisis estático la extrae directamente.

## Solución

### 1. Localizar el stack string

```bash
objdump -d -M intel s | grep -A50 '<main>'
```

23 instrucciones `mov BYTE PTR [rbp-0x20+i], imm8` construyen la cadena:

```
54 48 7b .. .. .. (23 bytes, terminando en 7d)
```

### 2. Decodificar

```python
raw = bytes([0x54, 0x48, 0x7b, 0x30, 0x62, 0x73, 0x65, 0x72,
             0x76, 0x34, 0x5f, 0x79, 0x5f, 0x33, 0x6e, 0x63,
             0x75, 0x33, 0x6e, 0x74, 0x72, 0x61, 0x7d])
print(raw.decode())
```

> 🚩 **Flag:** omitida intencionalmente. Seguí los pasos para obtenerla.

## Takeaways

- Stack strings: busca secuencias de `mov byte [rbp-x], imm` y convierte los inmediatos a ASCII.
- Una condición `argc > 9999` protege la salida en ejecución normal, pero no en el desensamblado.
- `objdump -d -M intel` + grep de inmediatos hexadecimales es suficiente para extraer la flag.

---
*Tropical Hunters CTF — Writeup por [Fabián Bustamante](https://github.com/fbustamante55)*
