# Common Pass

| | |
|---|---|
| **Categoría** | Crypto |
| **Dificultad** | Media |
| **Puntos** | 200 |
| **Reto #** | 43 |

## Descripción

`vault.txt` documenta AES-256-CBC con `kdf = sha256(password)`. La pista: *"everyone knows"* y *"nobody would guess"* → la contraseña está en `rockyou.txt`.

## Vulnerabilidad

**KDF débil: SHA-256 sin iteraciones ni sal** — SHA-256 es rápido por diseño (millones de hashes/segundo). Sin PBKDF2/bcrypt/Argon2 con sal, un diccionario de contraseñas comunes se prueba en segundos.

## Solución

```python
import hashlib, base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

iv = base64.b64decode("3YvfDb5Z0jaFjYCDSfjgnw==")
ct = base64.b64decode("3LiGvUVdR2A5FTwSj2qLBmyVxfI5Rug9k9RG1Zs2cvw=")

with open("/usr/share/wordlists/rockyou.txt", "rb") as f:
    for line in f:
        pwd = line.strip()
        key = hashlib.sha256(pwd).digest()
        try:
            cipher = AES.new(key, AES.MODE_CBC, iv)
            pt = unpad(cipher.decrypt(ct), 16)
            if b"TH{" in pt:
                print(f"Contraseña: {pwd.decode()}")
                print(pt.decode())
                break
        except Exception:
            continue
```

> 🚩 **Flag:** omitida intencionalmente. Seguí los pasos para obtenerla.

## Takeaways

- SHA-256 sin PBKDF2/bcrypt/Argon2 → ataque de diccionario viable en segundos con hardware moderno.
- KDF seguro mínimo: PBKDF2-HMAC-SHA256 con 600,000 iteraciones (NIST 2023) o Argon2id.
- `rockyou.txt` tiene ~14 millones de contraseñas reales; si la tuya está ahí, ya fue comprometida.

---
*Tropical Hunters CTF — Writeup por [Fabián Bustamante](https://github.com/fbustamante55)*
