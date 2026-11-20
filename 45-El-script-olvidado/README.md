# El script olvidado

| | |
|---|---|
| **Categoría** | Forensics |
| **Dificultad** | Fácil |
| **Puntos** | 50 |
| **Reto #** | 45 |

## Descripción

`mantenimiento.ps1` fue encontrado en una carpeta de incidente cerrado. El script parece rutinario pero una variable (`$notaCodificada`) guarda texto que no se lee directamente.

## Vulnerabilidad

**Ofuscación PowerShell con Base64** — la variable `$notaCodificada` contiene un string Base64. Es una técnica de ofuscación trivial: `[Convert]::FromBase64String` decodifica el contenido sin clave, en texto plano.

## Solución

**Nunca ejecutar scripts desconocidos.** Decodificar estáticamente:

```bash
echo "UmVjb3JkYXRvcmlvIGRlbCB0ZWNuaWNvOiBsYSBjbGF2ZSBkZWwgaW5jaWRlbnRlIGVzIFRIe3Bvd2Vyc2hlbGxfY29kaWZpY2Fkb19ub19jaWZyYWRvXzExfQ==" \
  | base64 -d
```

**En Python:**

```python
import base64
encoded = "UmVjb3JkYXRvcmlvIGRlbCB0ZWNuaWNvOiBsYSBjbGF2ZSBkZWwgaW5jaWRlbnRlIGVzIFRIe3Bvd2Vyc2hlbGxfY29kaWZpY2Fkb19ub19jaWZyYWRvXzExfQ=="
print(base64.b64decode(encoded).decode())
```

Salida: `Recordatorio del tecnico: la clave del incidente es TH{...}`

> 🚩 **Flag:** omitida intencionalmente. Seguí los pasos para obtenerla.

## Takeaways

- PowerShell `-EncodedCommand` y `[Convert]::FromBase64String` son indicadores clásicos de ofuscación.
- Regla forense: analizar el script **estáticamente** antes de ejecutar cualquier cosa.
- Detectores de IOC: buscar strings alfanuméricos de >50 caracteres terminados en `=` o `==` en scripts.

---
*Tropical Hunters CTF — Writeup por [Fabián Bustamante](https://github.com/fbustamante55)*
