# Evidencia comprimida

| | |
|---|---|
| **Categoría** | Forensics |
| **Dificultad** | Media |
| **Puntos** | 100 |
| **Reto #** | 49 |
| **Archivo** | `evidencia_estacion_07.zip` |

## Descripción

Un ZIP con cinco archivos de una estación de trabajo. Las notas del turno y el correo de soporte forman una cadena de pistas que apunta a un valor Base64 en el archivo de configuración.

## Solución

### 1. Inventariar el ZIP

```
evidencia_estacion_07.zip
├── LEEME.txt
├── notas_del_turno.txt       ← pista: "me respondieron por correo"
├── inventario.csv
├── correo_soporte.txt        ← pista: "el valor quedó en Base64 en app_config.ini"
└── config/
    └── app_config.ini        ← contiene el código de acceso
```

### 2. Leer `config/app_config.ini`

```ini
[usuario]
codigo_acceso = Q8OzZGln...
```

### 3. Decodificar

```bash
echo "Q8OzZGlnbyBkZSBhY2Nlc28gZGUgbGEgZXN0YWNpw7NuIDA3OiBUSHtkb3NfcGlzdGFzX3VuYV9yZXNwdWVzdGFfMjAyNn0uIE5vIGxvIGNvbXBhcnRhcyBjb24gbmFkaWUu" \
  | base64 -d
```

> 🚩 **Flag:** omitida intencionalmente. Seguí los pasos para obtenerla.

## Takeaways

- En forensics de texto plano: seguir la cadena de referencias entre archivos antes de buscar en binarios.
- Archivos de configuración son el primer lugar a revisar en un análisis forense de un endpoint.
- Base64 no es cifrado: `base64 -d` lo revierte instantáneamente; usar AES o similar para datos sensibles.

---
*Tropical Hunters CTF — Writeup por [Fabián Bustamante](https://github.com/fbustamante55)*
