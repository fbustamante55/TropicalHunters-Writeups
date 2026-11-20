# Big Bang

| | |
|---|---|
| **Categoría** | Reversing |
| **Dificultad** | Fácil |
| **Puntos** | 50 |
| **Reto #** | 21 |

## Descripción

"Todo gran destino empieza con un solo punto." El binario anima un universo; el secreto vive dentro del ejecutable mismo, pero no siempre es visible al ejecutarlo.

## Vulnerabilidad

**Flag en texto plano en sección `.rodata`** — el binario usa códigos de escape ANSI para hacer el texto invisible en un terminal oscuro. `strings` lo lee sin restricciones.

## Solución

### 1. Reconocimiento

```bash
file bigbang
# ELF 64-bit LSB PIE executable, x86-64, dynamically linked, not stripped
```

### 2. Extraer cadenas

```bash
strings bigbang | grep 'TH{'
```

La flag está almacenada en texto plano en `.rodata`. Los códigos `\033[33m` (amarillo) y `\033[30m` (negro sobre fondo oscuro) la hacen invisible al ejecutar el binario; `strings` los ignora y la expone directamente.

> 🚩 **Flag:** omitida intencionalmente. Seguí los pasos para obtenerla.

## Takeaways

- Primera acción en reversing: `strings | grep 'TH{'`.
- Una flag en texto plano no ofrece ninguna protección; el binario debe ofuscarla o calcularla en runtime para ocultarla.
- Los colores ANSI solo afectan la visualización en terminal, no el contenido real del binario.

---
*Tropical Hunters CTF — Writeup por [Fabián Bustamante](https://github.com/fbustamante55)*
