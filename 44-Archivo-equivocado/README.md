# Archivo equivocado

| | |
|---|---|
| **Categoría** | Forensics |
| **Dificultad** | Fácil |
| **Puntos** | 50 |
| **Reto #** | 44 |

## Descripción

Un ex-empleado dejó `informe_final.doc` en la carpeta del caso. Word lo rechaza como "dañado". La extensión fue cambiada deliberadamente para ocultar el tipo real.

## Vulnerabilidad

**Extensión falsa — file type confusion** — los sistemas operativos y algunas herramientas confían en la extensión; el tipo real se determina por el **magic number** (firma de bytes al inicio del archivo).

## Solución

### 1. Verificar el tipo real

```bash
file informe_final.doc
# informe_final.doc: PNG image data, 800 x 437, 8-bit/color RGBA

xxd informe_final.doc | head -1
# 89504e47 0d0a1a0a  → firma PNG (\x89PNG)
```

### 2. Renombrar y abrir

```bash
cp informe_final.doc informe_final.png
# Abrir como imagen → memorando interno con la flag
```

### 3. Magic numbers comunes

| Tipo | Firma hex | ASCII |
|------|-----------|-------|
| PNG | `89 50 4E 47` | `\x89PNG` |
| JPEG | `FF D8 FF` | — |
| PDF | `25 50 44 46` | `%PDF` |
| ZIP | `50 4B 03 04` | `PK..` |
| ELF | `7F 45 4C 46` | `.ELF` |

> 🚩 **Flag:** omitida intencionalmente. Seguí los pasos para obtenerla.

## Takeaways

- Nunca confiar en la extensión para determinar el tipo de archivo; usar `file` o leer el magic number.
- En forense digital: `file`, `xxd | head`, `binwalk` como triada inicial de análisis.
- Cambiar la extensión es una técnica de evasión básica; los AV modernos y los SIEM la detectan.

---
*Tropical Hunters CTF — Writeup por [Fabián Bustamante](https://github.com/fbustamante55)*
