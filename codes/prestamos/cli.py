from __future__ import annotations

import logging
from typing import Any

from prestamos.config import ROLE_ENCARGADO, configurar_directorios
from prestamos.usuarios import iniciar_sesion


def menu_solicitante(usuario: dict[str, Any]) -> None:
    while True:
        print(
            """
========== MENÚ SOLICITANTE ==========

0. Cerrar sesión
"""
        )
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "0":
            logging.info("Sesión cerrada | correo=%s", usuario["correo"])
            return
        else:
            print("Opción inválida.")


def menu_encargado(usuario: dict[str, Any]) -> None:
    from prestamos.usuarios import (
        activar_desactivar_usuario,
        listar_usuarios,
        registrar_usuario,
    )

    while True:
        print(
            """
=========== MENÚ ENCARGADO ===========

1. Registrar usuario
2. Listar usuarios
3. Activar/desactivar usuario

0. Cerrar sesión
"""
        )
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            registrar_usuario(usuario)
        elif opcion == "2":
            listar_usuarios(usuario)
        elif opcion == "3":
            activar_desactivar_usuario(usuario)
        elif opcion == "0":
            logging.info("Sesión cerrada | correo=%s", usuario["correo"])
            return
        else:
            print("Opción inválida.")


def main() -> None:
    configurar_directorios()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

    print("=====================================")
    print(" SISTEMA DE PRÉSTAMO DE EQUIPOS")
    print("=====================================")

    while True:
        print(
            """
1. Iniciar sesión
0. Salir
"""
        )
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            usuario = iniciar_sesion()

            if usuario is None:
                continue

            if usuario["rol"] == ROLE_ENCARGADO:
                menu_encargado(usuario)
            else:
                menu_solicitante(usuario)

        elif opcion == "0":
            print("Programa finalizado.")
            break

        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()
