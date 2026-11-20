# Registro nocturno

| | |
|---|---|
| **Categoría** | Forensics |
| **Dificultad** | Fácil |
| **Puntos** | 50 |
| **Reto #** | 47 |

## Descripción

Un servidor registra cada login. El administrador reportó actividad extraña en la madrugada del 14 al 15 de marzo de 2026. El log tiene cientos de líneas normales; hay una que no encaja.

## Solución

### 1. Filtrar por anomalías

```bash
# Nivel ALERT (el único en todo el archivo)
grep ALERT servidor_nocturno.log

# IP fuera de la subred interna 192.168.10.0/24
grep "10.0.99" servidor_nocturno.log
```

Línea anómala encontrada:

```
2026-03-15 03:00:07 [ALERT] auth user=admin src=10.0.99.66 action=login
result=ok nota=acceso_fuera_de_horario_desde_ip_desconocida
mensaje="VEh7..."
```

### 2. Decodificar el campo `mensaje`

```bash
echo "VEh7..." | base64 -d
```

### 3. Señales de compromiso identificadas

| Señal | Detalle |
|-------|---------|
| IP externa | `10.0.99.66` fuera de `192.168.10.0/24` |
| Fuerza bruta | 4 intentos fallidos entre 02:58–02:59 |
| Horario | Acceso exitoso a las 03:00 (`acceso_fuera_de_horario`) |
| Único `[ALERT]` | Nivel más alto en todo el log |

> 🚩 **Flag:** omitida intencionalmente. Seguí los pasos para obtenerla.

## Takeaways

- Estrategia de triaje: nivel `[ALERT/ERROR/CRIT]` → IPs fuera de rango → horarios inusuales.
- Patrón brute-force clásico: múltiples `result=fail` → un `result=ok` desde la misma IP.
- Campos Base64 en logs (`mensaje`, `token`, `data`) son vectores de exfiltración o evidencia CTF.

---
*Tropical Hunters CTF — Writeup por [Fabián Bustamante](https://github.com/fbustamante55)*
