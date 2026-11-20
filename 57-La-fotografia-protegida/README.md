# La fotografía protegida

| | |
|---|---|
| **Categoría** | Stego / Forensics |
| **Dificultad** | Media |
| **Puntos** | 100 |
| **Reto #** | 57 |

## Descripción

`retrato_final.jpg` tiene dos capas de secreto: un ZIP embebido (igual que reto 54) **y** una contraseña que el fotógrafo guardó en los metadatos EXIF de la misma imagen.

## Vulnerabilidad

**Polyglot JPEG + ZIP cifrado con contraseña en EXIF** — la contraseña se extrae de los metadatos, y con ella se descomprime el ZIP que contiene la flag.

## Solución

### 1. Extraer la contraseña desde EXIF

```bash
exiftool retrato_final.jpg | grep -i 'comment\|user\|description'
# UserComment: acceso_secreto_foto
```

**Sin exiftool:**

```python
import subprocess
result = subprocess.run(['strings', '-n', '5', 'retrato_final.jpg'],
                       capture_output=True, text=True)
for line in result.stdout.splitlines():
    if 5 < len(line) < 30 and line.isascii() and '_' in line:
        print(line)
# acceso_secreto_foto
```

### 2. Extraer el ZIP embebido

```python
d = open('retrato_final.jpg', 'rb').read()
eoi = d.rfind(b'\xff\xd9')
open('oculto.zip', 'wb').write(d[eoi + 2:])
```

### 3. Descomprimir con contraseña

```bash
unzip -P acceso_secreto_foto oculto.zip
cat archivos/mensaje_privado.txt
```

> 🚩 **Flag:** omitida intencionalmente. Seguí los pasos para obtenerla.

## Takeaways

- Combinar dos técnicas (polyglot + metadatos) no multiplica la seguridad si ambas son trivialmente analizables.
- `exiftool` es el estándar forense para metadatos EXIF; alternativa: `strings` para campos de texto corto.
- Flujo de análisis de imagen: `file` → `binwalk` → `exiftool` → `strings` → datos tras EOI.

---
*Tropical Hunters CTF — Writeup por [Fabián Bustamante](https://github.com/fbustamante55)*
