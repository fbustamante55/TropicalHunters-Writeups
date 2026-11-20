# Fragmentos de color

| | |
|---|---|
| **Categoría** | Stego / Imagen |
| **Dificultad** | Media |
| **Puntos** | 100 |
| **Reto #** | 55 |

## Descripción

`obra_prisma.png` (pintura abstracta 900×400). *"No todo lo que pinto se ve a simple vista."* El mensaje está en el bit menos significativo del canal azul.

## Vulnerabilidad

**Esteganografía LSB — canal azul** — el bit 0 de cada píxel del canal B almacena un bit del mensaje. El cambio es de ±1 en el valor del color, imperceptible al ojo humano pero detectable al extraer el plano de bit 0.

## Solución

### Extracción con Python

```python
from PIL import Image
import numpy as np

img = np.array(Image.open('obra_prisma.png'))

# Extraer y visualizar el plano LSB de cada canal
for canal, nombre in [(0,'R'), (1,'G'), (2,'B')]:
    for bit in range(3):
        plano = ((img[:,:,canal] >> bit) & 1) * 255
        Image.fromarray(plano.astype('uint8')).save(f'plano_{nombre}_bit{bit}.png')
```

El archivo `plano_B_bit0.png` muestra texto visible en la mitad inferior izquierda.

### Alternativas

```bash
zsteg obra_prisma.png          # detecta LSB automáticamente
# StegSolve → Blue plane 0
```

> 🚩 **Flag:** omitida intencionalmente. Seguí los pasos para obtenerla.

## Takeaways

- LSB visual: revisar los 9 planos (R/G/B × bit 0/1/2) antes de probar métodos más complejos.
- `zsteg` automatiza la detección de LSB en PNG en < 1 segundo.
- Esteganografía LSB no ofrece seguridad sin estegokey — es solo ocultación, no cifrado.

---
*Tropical Hunters CTF — Writeup por [Fabián Bustamante](https://github.com/fbustamante55)*
