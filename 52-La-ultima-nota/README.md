# La última nota

| | |
|---|---|
| **Categoría** | Forensics / Metadatos |
| **Dificultad** | Fácil |
| **Puntos** | 50 |
| **Reto #** | 52 |

## Descripción

Un fotógrafo desapareció dejando `ultima_foto.jpg`. Siempre anotaba sus imágenes. La flag está en los metadatos EXIF, en el campo `UserComment`, codificada en Base64.

## Solución

### 1. Extraer metadatos

```bash
exiftool ultima_foto.jpg | grep -i 'comment\|user\|description'
# UserComment: VEh7...
```

**Alternativa sin exiftool:**

```bash
strings -n 20 ultima_foto.jpg | grep -E '^[A-Za-z0-9+/]{20,}={0,2}$'
```

### 2. Decodificar

```bash
echo "VEh7..." | base64 -d
```

> 🚩 **Flag:** omitida intencionalmente. Seguí los pasos para obtenerla.

## Takeaways

- Flujo forense básico en imágenes: `file` → `strings` → `exiftool` → buscar datos tras EOI.
- El campo EXIF `UserComment` acepta datos arbitrarios; los visores de fotos lo ocultan.
- Los metadatos revelan modelo de cámara, GPS, software usado — datos valiosos en investigaciones reales.

---
*Tropical Hunters CTF — Writeup por [Fabián Bustamante](https://github.com/fbustamante55)*
