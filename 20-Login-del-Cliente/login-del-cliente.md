# Login del Cliente (Web, 50 pts, 1 solve)

**Flag:** `TH{REDACTED}`

## Enunciado
Portal de clientes de Cafetal Cloud: "tu contraseña nunca sale de tu navegador", por lo que el login se valida sin servidor. Se entrega `login.html`; si aparece "Acceso concedido", la contraseña escrita es la flag.

## Solución
1. Ver el código fuente de la página: la validación está en JavaScript del lado del cliente, en `validarClave(clave)`.
2. La función exige longitud 38 y compara fragmentos con `substring`, listados en desorden:
   - `[0:2]` = `TH`
   - `[2:7]` = `{el_n`
   - `[7:12]` = `avega`
   - `[12:17]` = `dor_n`
   - `[17:22]` = `o_gua`
   - `[22:26]` = `rda_`
   - `[26:30]` = `secr`
   - `[30:34]` = `etos`
   - `[34:38]` = `_52}`
3. Ordenar por posición y concatenar: `TH{REDACTED}` (38 caracteres; verificado contra todas las comparaciones).

## Lecciones / técnica
- Una validación de contraseña en el cliente expone el secreto en el código fuente (Ver código fuente / DevTools); no es seguridad.
- Las comparaciones en desorden solo dificultan leerlo a ojo; se reconstruye ordenando por índice.
- Se resolvió leyendo el HTML, sin ejecutarlo en un navegador.
