from __future__ import annotations

import logging
from typing import Any

from prestamos.config import ROLE_ENCARGADO, configurar_directorios
from prestamos.usuarios import iniciar_sesion


def menu_solicitante(usuario: dict[str, Any]) -> None:
    from prestamos.equipos import listar_equipos
    from prestamos.solicitudes import consultar_mis_solicitudes, crear_solicitud

    while True:
        print(
            """
========== MENÚ SOLICITANTE ==========

1. Consultar equipos
2. Crear solicitud
3. Consultar mis solicitudes

0. Cerrar sesión
"""
        )
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            listar_equipos()
        elif opcion == "2":
            crear_solicitud(usuario)
        elif opcion == "3":
            consultar_mis_solicitudes(usuario)
        elif opcion == "0":
            logging.info("Sesión cerrada | correo=%s", usuario["correo"])
            return
        else:
            print("Opción inválida.")


def menu_encargado(usuario: dict[str, Any]) -> None:
    from prestamos.equipos import (
        activar_desactivar_equipo,
        listar_equipos,
        registrar_equipo,
    )
    from prestamos.solicitudes import (
        consultar_mis_solicitudes,
        consultar_todas_solicitudes,
        crear_solicitud,
    )
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

4. Registrar equipo
5. Consultar equipos
6. Activar/desactivar equipo

7. Crear solicitud personal
8. Consultar mis solicitudes
9. Consultar todas las solicitudes

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
        elif opcion == "4":
            registrar_equipo(usuario)
        elif opcion == "5":
            listar_equipos()
        elif opcion == "6":
            activar_desactivar_equipo(usuario)
        elif opcion == "7":
            crear_solicitud(usuario)
        elif opcion == "8":
            consultar_mis_solicitudes(usuario)
        elif opcion == "9":
            consultar_todas_solicitudes(usuario)
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
