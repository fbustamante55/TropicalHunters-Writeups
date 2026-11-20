# Mensaje del fotógrafo

| | |
|---|---|
| **Categoría** | Forensics / Metadatos |
| **Dificultad** | Fácil |
| **Puntos** | 50 |
| **Reto #** | 53 |

## Descripción

`reportaje.jpg` (foto nocturna urbana) pertenece a un periodista desaparecido. Siempre anotaba sus imágenes. La flag está en el campo EXIF `ImageDescription`, en Base64.

## Solución

### 1. Extraer metadatos

```bash
exiftool reportaje.jpg | grep -i 'description\|comment'
# Image Description: Tm90YSBkZWwgcGVyaW9kaXN0YS4u...
```

**Alternativa con strings:**

```bash
strings -n 10 reportaje.jpg \
  | grep -E '^[A-Za-z0-9+/]{20,}={0,2}$'
```

### 2. Decodificar

```bash
echo "Tm90YSBkZWwgcGVyaW9kaXN0YTogc2kgZW5jdWVudHJhcyBlc3RvLCBsYSBjbGF2ZSBkZWwgcmVwb3J0YWplIGVzIFRIe2Jhc2U2NF9ub19lc19jaWZyYWRvXzY0fQ==" \
  | base64 -d
```

> 🚩 **Flag:** omitida intencionalmente. Seguí los pasos para obtenerla.

## Takeaways

- Base64 en metadatos EXIF (`ImageDescription`) es un canal oculto trivial: `strings` o `exiftool` lo exponen.
- **Base64 ≠ cifrado**: es solo representación de datos en caracteres imprimibles. No ofrece confidencialidad.
- Para proteger datos en metadatos se requiere cifrado real (AES) + eliminación del campo antes de publicar.

---
*Tropical Hunters CTF — Writeup por [Fabián Bustamante](https://github.com/fbustamante55)*
