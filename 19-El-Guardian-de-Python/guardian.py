#!/usr/bin/env python3
# El Guardián de la puerta secreta.
# Solo quien conozca la contraseña correcta podrá pasar.

import base64

# Lo único que el guardián recuerda de la contraseña.
SECRETO = "fTcyX2F0cmV1cF9hbF9lcmJhX29naWRvY19sZV9yZWVse0hU"


def preparar(intento):
    # El guardián tiene sus propias costumbres...
    volteado = intento[::-1]
    return base64.b64encode(volteado.encode()).decode()


def main():
    print("Soy el Guardián. Nadie cruza esta puerta sin la contraseña.")
    intento = input("Contraseña: ").strip()
    if preparar(intento) == SECRETO:
        print("Acceso concedido. La puerta se abre lentamente...")
    else:
        print("Acceso denegado. El Guardián no se mueve.")


if __name__ == "__main__":
    main()
