from __future__ import annotations

import logging
from typing import Any

from prestamos.config import ROLE_ENCARGADO, ROLE_SOLICITANTE, USERS_FILE
from prestamos.persistencia import (
    cargar_json,
    guardar_json,
    hash_password,
    leer_no_vacio,
)


def buscar_usuario_por_correo(correo: str) -> dict[str, Any] | None:
    usuarios = cargar_json(USERS_FILE)

    return next(
        (u for u in usuarios if u["correo"].lower() == correo.lower()),
        None,
    )


def buscar_usuario_por_rut(rut: str) -> dict[str, Any] | None:
    usuarios = cargar_json(USERS_FILE)

    return next((u for u in usuarios if u["rut"] == rut), None)


def registrar_usuario(usuario_actual: dict[str, Any]) -> None:
    """RN-01: solo un Encargado puede registrar nuevos usuarios."""
    if usuario_actual["rol"] != ROLE_ENCARGADO:
        print("Acceso denegado: solo un Encargado puede registrar usuarios.")
        return

    usuarios = cargar_json(USERS_FILE)

    nombre = leer_no_vacio("Nombre: ")
    rut = leer_no_vacio("RUT: ")
    correo = leer_no_vacio("Correo electrónico: ").lower()
    password = leer_no_vacio("Contraseña: ")

    print("\n1. Solicitante")
    print("2. Encargado")
    opcion = input("Seleccione el rol: ").strip()

    if opcion == "1":
        rol = ROLE_SOLICITANTE
    elif opcion == "2":
        rol = ROLE_ENCARGADO
    else:
        print("Rol inválido.")
        return

    if buscar_usuario_por_rut(rut):
        print("Ya existe un usuario con ese RUT.")
        return

    if buscar_usuario_por_correo(correo):
        print("Ya existe un usuario con ese correo.")
        return

    nuevo_usuario = {
        "nombre": nombre,
        "rut": rut,
        "correo": correo,
        "password_hash": hash_password(password),
        "rol": rol,
        "activo": True,
    }

    usuarios.append(nuevo_usuario)

    if guardar_json(USERS_FILE, usuarios):
        logging.info(
            "Usuario registrado | correo=%s | rol=%s | registrado_por=%s",
            correo,
            rol,
            usuario_actual["correo"],
        )
        print("Usuario registrado correctamente.")


def listar_usuarios(usuario_actual: dict[str, Any]) -> None:
    if usuario_actual["rol"] != ROLE_ENCARGADO:
        print("Acceso denegado.")
        return

    usuarios = cargar_json(USERS_FILE)

    if not usuarios:
        print("No existen usuarios registrados.")
        return

    print("\n--- USUARIOS ---")
    for usuario in usuarios:
        estado = "Activo" if usuario["activo"] else "Inactivo"
        print(
            f"{usuario['nombre']} | RUT: {usuario['rut']} | "
            f"{usuario['correo']} | {usuario['rol']} | {estado}"
        )


def activar_desactivar_usuario(usuario_actual: dict[str, Any]) -> None:
    if usuario_actual["rol"] != ROLE_ENCARGADO:
        print("Acceso denegado.")
        return

    correo = leer_no_vacio("Correo del usuario: ").lower()
    usuarios = cargar_json(USERS_FILE)

    usuario_objetivo = next(
        (u for u in usuarios if u["correo"].lower() == correo),
        None,
    )

    if usuario_objetivo is None:
        print("Usuario no encontrado.")
        return

    if usuario_objetivo["correo"] == usuario_actual["correo"]:
        print("No puede desactivar su propia cuenta mientras mantiene la sesión iniciada.")
        return

    usuario_objetivo["activo"] = not usuario_objetivo["activo"]

    if guardar_json(USERS_FILE, usuarios):
        logging.info(
            "Estado de usuario modificado | correo=%s | activo=%s | por=%s",
            usuario_objetivo["correo"],
            usuario_objetivo["activo"],
            usuario_actual["correo"],
        )
        print("Usuario activado." if usuario_objetivo["activo"] else "Usuario desactivado.")


def iniciar_sesion() -> dict[str, Any] | None:
    """RN-02: solo usuarios registrados y activos pueden iniciar sesión."""
    correo = leer_no_vacio("Correo electrónico: ").lower()
    password = leer_no_vacio("Contraseña: ")

    usuario = buscar_usuario_por_correo(correo)

    if usuario is None:
        logging.warning("Inicio de sesión rechazado | usuario inexistente | correo=%s", correo)
        print("Credenciales incorrectas.")
        return None

    if not usuario.get("activo", False):
        logging.warning("Inicio de sesión rechazado | usuario inactivo | correo=%s", correo)
        print("El usuario se encuentra inactivo.")
        return None

    if usuario["password_hash"] != hash_password(password):
        logging.warning("Inicio de sesión rechazado | contraseña incorrecta | correo=%s", correo)
        print("Credenciales incorrectas.")
        return None

    logging.info("Inicio de sesión exitoso | correo=%s", correo)
    print(f"\nBienvenido/a {usuario['nombre']} ({usuario['rol']})")

    return usuario
