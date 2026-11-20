# Imagen sospechosa

| | |
|---|---|
| **Categoría** | Misc / Stego |
| **Dificultad** | Fácil-Media |
| **Puntos** | 100 |
| **Reto #** | 51 |

## Descripción

`banner_portal.jpg` parece una imagen corporativa normal. El analista dejó una nota: *"no te fíes de lo que muestra la pantalla."* La flag está oculta **después** del marcador de fin de JPEG (`FF D9`), en Base64.

## Vulnerabilidad

**Datos annexados tras el EOI de JPEG** — los visores ignoran todo lo posterior al marcador `FF D9`; los bytes siguen presentes en el archivo y `strings` los expone.

## Solución

### 1. Verificar el archivo

```bash
file banner_portal.jpg   # JPEG válido
strings banner_portal.jpg | grep -v '^[^A-Za-z]*$' | tail -20
```

Al final de las strings aparece:

```
-- nota interna --
Codigo (base64): VEh7...
```

### 2. Decodificar

```bash
echo "VEh7..." | base64 -d
```

### 3. Verificar la posición en el archivo

```bash
# El marcador FF D9 está en un offset; lo que sigue es la nota
python3 -c "
d = open('banner_portal.jpg','rb').read()
eoi = d.rfind(b'\xff\xd9')
print(d[eoi+2:].decode('utf-8', errors='ignore'))
"
```

> 🚩 **Flag:** omitida intencionalmente. Seguí los pasos para obtenerla.

## Takeaways

- JPEG termina en `FF D9`; todo lo posterior es ignorado por visores pero accesible en el archivo.
- `strings` como primer paso en análisis de imágenes: detecta texto embebido sin herramientas especiales.
- Variante más sofisticada: esteganografía LSB (reto 55) que modifica píxeles y no es detectable con `strings`.

---
*Tropical Hunters CTF — Writeup por [Fabián Bustamante](https://github.com/fbustamante55)*
