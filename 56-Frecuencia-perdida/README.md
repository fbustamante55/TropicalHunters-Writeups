# Frecuencia perdida

| | |
|---|---|
| **Categoría** | Stego / Audio |
| **Dificultad** | Media |
| **Puntos** | 100 |
| **Reto #** | 56 |

## Descripción

`transmision_secreta.wav` suena como ruido blanco. La pista: *"lo que necesitas está entre las frecuencias."* El mensaje está escrito en el espectrograma.

## Vulnerabilidad

**Esteganografía en espectrograma** — el mensaje fue sintetizado como tonos en frecuencias específicas, formando texto legible al graficar la representación tiempo-frecuencia (STFT). La reproducción normal solo suena como ruido.

## Solución

### Opción A — Audacity (GUI)

```
View → Spectrogram
Escala: logarítmica, ventana 2048 muestras
```

### Opción B — Python (sin GUI)

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import spectrogram

sr, data = wavfile.read('transmision_secreta.wav')
if data.ndim > 1:
    data = data[:,0]

f, t, Sxx = spectrogram(data, fs=sr, nperseg=1024, noverlap=896)

plt.figure(figsize=(20, 6))
plt.pcolormesh(t, f, 10*np.log10(Sxx + 1e-10),
               shading='gouraud', cmap='inferno')
plt.ylim(0, 8000)
plt.ylabel('Frecuencia (Hz)')
plt.xlabel('Tiempo (s)')
plt.savefig('espectrograma.png', dpi=150, bbox_inches='tight')
print("Guardado: espectrograma.png")
```

El espectrograma muestra el texto de la flag (`TH{...}`) en la banda 2000–5000 Hz.

> 🚩 **Flag:** omitida intencionalmente. Seguí los pasos para obtenerla.

## Takeaways

- Espectrograma = representación visual de energía por frecuencia a lo largo del tiempo; texto sintetizado es visible directamente.
- Sonic Visualiser o Audacity son las herramientas estándar; scipy + matplotlib dan el mismo resultado programáticamente.
- Variante real: malware que exfiltra datos modulando audio; esta técnica se ha documentado en ataques reales.

---
*Tropical Hunters CTF — Writeup por [Fabián Bustamante](https://github.com/fbustamante55)*
