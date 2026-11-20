# El paquete secreto

| | |
|---|---|
| **Categoría** | Stego / Forensics |
| **Dificultad** | Media |
| **Puntos** | 100 |
| **Reto #** | 54 |

## Descripción

`boceto_final.jpg` lleva "más de lo que una imagen debería llevar." Después del marcador `FF D9` (fin de JPEG) hay 750 bytes con la firma `PK` de un archivo ZIP.

## Vulnerabilidad

**Polyglot JPEG + ZIP** — los visores de imágenes ignoran todo lo posterior al último `FF D9`; `unzip` lee el archivo desde la firma `PK` hacia adelante. El archivo funciona como JPEG Y como ZIP simultáneamente.

## Solución

### 1. Detectar el ZIP embebido

```bash
file boceto_final.jpg          # JPEG válido
binwalk boceto_final.jpg       # detecta firma ZIP en offset 0xC479
xxd boceto_final.jpg | grep -A1 'ff d9'
# offset 0xC479: 50 4b 03 04  → PK (ZIP)
```

### 2. Extraer el ZIP

```python
d = open('boceto_final.jpg', 'rb').read()
eoi = d.rfind(b'\xff\xd9')
open('oculto.zip', 'wb').write(d[eoi + 2:])
```

**Alternativa:**

```bash
unzip boceto_final.jpg   # unzip lee desde la firma PK automáticamente
```

### 3. Leer el contenido

```bash
unzip oculto.zip
cat paquete/mensaje_de_la_disenadora.txt
```

> 🚩 **Flag:** omitida intencionalmente. Seguí los pasos para obtenerla.

## Takeaways

- `binwalk` detecta firmas de múltiples formatos en un solo archivo en segundos.
- `unzip` lee desde la firma `PK` sin importar lo que haya antes — explotar esto es trivial.
- Variante con contraseña: reto 57; la contraseña está en los metadatos EXIF de la misma imagen.

---
*Tropical Hunters CTF — Writeup por [Fabián Bustamante](https://github.com/fbustamante55)*
