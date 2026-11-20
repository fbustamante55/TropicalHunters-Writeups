# Login del Cliente

| | |
|---|---|
| **Categoría** | Web |
| **Dificultad** | Fácil |
| **Puntos** | 50 |
| **Reto #** | 20 |

## Descripción

Un portal de cliente pide credenciales. La lógica de autenticación no vive en el servidor sino en el navegador. Leer el código fuente del frontend revela las credenciales y la flag.

## Vulnerabilidad

**Autenticación del lado del cliente (CWE-603)**

La aplicación valida usuario y contraseña mediante JavaScript ejecutado en el navegador. Cualquier persona puede inspeccionar el código con DevTools y ver las credenciales en texto plano, junto con la flag embebida en la lógica.

## Solución

### 1. Abrir DevTools → Sources

Buscar el archivo JS principal del login (generalmente `app.js`, `main.js` o similar).

### 2. Buscar la lógica de validación

```js
// Ejemplo de lo que se encuentra:
if (username === "cliente" && password === "secreto123") {
    showFlag("TH{...}");
}
```

### 3. Alternativa — búsqueda directa

```bash
# Descargar el JS y buscar la flag
curl http://<instancia>/static/app.js | grep -o 'TH{[^}]*}'
```

> 🚩 **Flag:** omitida intencionalmente. Seguí los pasos para obtenerla.

## Takeaways

- Nunca realizar validaciones de seguridad únicamente en el cliente: todo JavaScript es visible al usuario.
- Las credenciales y la lógica de autenticación deben vivir exclusivamente en el servidor.
- Revisión de código fuente del frontend es siempre el primer paso en un reto de web.

---
*Tropical Hunters CTF — Writeup por [Fabián Bustamante](https://github.com/fbustamante55)*
