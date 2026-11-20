# La fotografía protegida (Stego, 100 pts, 4 solves)

**Flag:** `TH{REDACTED}`

## Enunciado
Proyecto Aurora: se entrega `expedicion.jpg` (foto del campamento base, glaciar norte) y la frase "Todo lo que necesitan está dentro de la foto, incluida la llave". Objetivo: recuperar el diario de campo oculto y leer el código de verificación.

## Solución
1. **Identificar el archivo:** `file expedicion.jpg` muestra JPEG 800x600 con EXIF (AuroraCam AC-200, fecha 2026:03:14 09:30:00).
2. **Metadatos / strings:** `strings -n 6 expedicion.jpg` revela, entre los campos de texto, la línea `Clave del archivo adjunto: aurora-glaciar-2026`. Esa es la llave.
3. **Datos anexos:** buscando el último marcador de fin de imagen (`FF D9`, offset 75828) hay 613 bytes después. A partir del offset 75830 aparece la firma `PK\x03\x04`: un ZIP cifrado pegado al JPEG (contiene `diario_de_campo.txt`).
4. **Extracción:**
   ```python
   d = open('expedicion.jpg','rb').read()
   open('a.zip','wb').write(d[75830:])
   ```
   `unzip -P aurora-glaciar-2026 a.zip` → `diario_de_campo.txt`.
5. **Diario:** entrada del día 6 (14/03/2026): grieta de 42 m de profundidad, retroceso de 11 m de la lengua del glaciar. Contiene el código de verificación: `TH{REDACTED}`.

## Lecciones / técnica
- Archivo polyglot: JPEG + ZIP concatenado (los visores ignoran lo posterior a `FFD9`).
- Revisar siempre metadatos y `strings` por contraseñas; buscar firmas (`PK`, `Rar!`, `7z`) tras el EOI.
- No hizo falta binwalk/steghide (no estaban instalados); bastó Python.
