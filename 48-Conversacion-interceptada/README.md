# Conversación interceptada

| | |
|---|---|
| **Categoría** | Forensics |
| **Dificultad** | Media |
| **Puntos** | 100 |
| **Reto #** | 48 |
| **Archivo** | `captura_incidente.pcap` |

## Descripción

Captura de tráfico de red interna de NovaTech Labs. HTTP en texto plano sobre el puerto 80; la flag viaja sin cifrado en el cuerpo de una respuesta.

## Solución

### 1. Wireshark — filtrar HTTP

```
http
```

### 2. Follow TCP Stream

Paquete 13 (`10.0.0.5 → 192.168.50.12`, HTTP 200 OK): el cuerpo HTML contiene:

```html
<p><strong>VEh7...</strong></p>
```

### 3. Decodificar

```bash
echo "VEh7..." | base64 -d
```

**Alternativa con tshark:**

```bash
tshark -r captura_incidente.pcap -Y http -T fields -e http.file_data \
  | grep -o 'VEh[A-Za-z0-9+/=]*' | base64 -d
```

> 🚩 **Flag:** omitida intencionalmente. Seguí los pasos para obtenerla.

## Takeaways

- HTTP (puerto 80) no cifra el contenido: cualquier dispositivo en el camino puede leer todo.
- `Follow TCP Stream` en Wireshark reconstruye la conversación completa entre dos endpoints.
- Mitigación: forzar HTTPS con HSTS (`Strict-Transport-Security`) y redireccionamiento 301 permanente.

---
*Tropical Hunters CTF — Writeup por [Fabián Bustamante](https://github.com/fbustamante55)*
