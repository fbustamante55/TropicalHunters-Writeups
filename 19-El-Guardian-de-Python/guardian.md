# Guardián (Reversing/Python, `guardian.py`)

**Flag:** `TH{REDACTED}`

## Enunciado
Un guardián en Python pide una contraseña y solo deja pasar a la correcta. El código fuente está a la vista y el autor dice que la contraseña no está escrita ahí. La contraseña es la flag.

## Solución
1. El programa compara `preparar(intento) == SECRETO`, con:
   ```python
   def preparar(intento):
       volteado = intento[::-1]
       return base64.b64encode(volteado.encode()).decode()
   SECRETO = "fTcyX2F0cmV1cF9hbF9lcmJhX29naWRvY19sZV9yZWVse0hU"
   ```
2. Es una transformación reversible: primero se invierte la cadena y luego se codifica en base64. Para deshacerla se hace en orden inverso: decodificar base64 y volver a invertir.
   ```python
   base64.b64decode(SECRETO).decode()[::-1]
   ```
3. Resultado: `TH{REDACTED}`. Comprobado: `preparar(flag) == SECRETO` da `True`.

## Lecciones / técnica
- Comparar contra un valor "ofuscado" con una transformación reversible (base64 + reverse) no protege nada: el secreto se recupera aplicando la inversa.
- Una contraseña real debería compararse contra un hash con sal (bcrypt, scrypt), que no es reversible.
