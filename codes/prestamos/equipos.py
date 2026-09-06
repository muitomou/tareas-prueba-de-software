from __future__ import annotations

import logging
from typing import Any

from prestamos.config import EQUIPMENT_FILE, ROLE_ENCARGADO
from prestamos.persistencia import cargar_json, guardar_json, leer_no_vacio


def buscar_equipo(equipo_id: str) -> dict[str, Any] | None:
    equipos = cargar_json(EQUIPMENT_FILE)

    return next((e for e in equipos if e["id"] == equipo_id), None)


def registrar_equipo(usuario_actual: dict[str, Any]) -> None:
    if usuario_actual["rol"] != ROLE_ENCARGADO:
        print("Acceso denegado: solo un Encargado puede registrar equipos.")
        return

    equipos = cargar_json(EQUIPMENT_FILE)

    equipo_id = leer_no_vacio("Identificador único del equipo: ")

    if buscar_equipo(equipo_id):
        print("Ya existe un equipo con ese identificador.")
        return

    nombre = leer_no_vacio("Nombre del equipo: ")
    descripcion = input("Descripción: ").strip()

    nuevo_equipo = {
        "id": equipo_id,
        "nombre": nombre,
        "descripcion": descripcion,
        "activo": True,
    }

    equipos.append(nuevo_equipo)

    if guardar_json(EQUIPMENT_FILE, equipos):
        logging.info(
            "Equipo registrado | id=%s | por=%s",
            equipo_id,
            usuario_actual["correo"],
        )
        print("Equipo registrado correctamente.")


def listar_equipos() -> None:
    equipos = cargar_json(EQUIPMENT_FILE)

    if not equipos:
        print("No existen equipos registrados.")
        return

    print("\n--- EQUIPOS ---")
    for equipo in equipos:
        estado = "Activo" if equipo["activo"] else "Inactivo"
        print(f"{equipo['id']} | {equipo['nombre']} | {estado}")


def activar_desactivar_equipo(usuario_actual: dict[str, Any]) -> None:
    if usuario_actual["rol"] != ROLE_ENCARGADO:
        print("Acceso denegado.")
        return

    equipo_id = leer_no_vacio("ID del equipo: ")
    equipos = cargar_json(EQUIPMENT_FILE)

    equipo_objetivo = next((e for e in equipos if e["id"] == equipo_id), None)

    if equipo_objetivo is None:
        print("Equipo no encontrado.")
        return

    equipo_objetivo["activo"] = not equipo_objetivo["activo"]

    if guardar_json(EQUIPMENT_FILE, equipos):
        logging.info(
            "Estado del equipo modificado | id=%s | activo=%s | por=%s",
            equipo_id,
            equipo_objetivo["activo"],
            usuario_actual["correo"],
        )
        print("Equipo activado." if equipo_objetivo["activo"] else "Equipo desactivado.")
