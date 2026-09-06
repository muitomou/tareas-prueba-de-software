from __future__ import annotations

import logging
from datetime import date, datetime
from typing import Any

from prestamos.config import (
    EQUIPMENT_FILE,
    ESTADO_APROBADA,
    ESTADO_ATRASADA,
    ESTADO_DEVUELTA,
    ESTADO_ENTREGADA,
    REQUESTS_FILE,
    ROLE_ENCARGADO,
    ROLE_SOLICITANTE,
    USERS_FILE,
)
from prestamos.persistencia import cargar_json, guardar_json, hash_password, leer_entero
from prestamos.solicitudes import actualizar_estados_automaticos, imprimir_solicitud


def _buscar_solicitud(solicitudes: list[dict[str, Any]], solicitud_id: int) -> dict[str, Any] | None:
    return next((s for s in solicitudes if s["id"] == solicitud_id), None)


def registrar_entrega(usuario_actual: dict[str, Any]) -> None:
    """RN-08: solo se entrega una solicitud que está Aprobada."""
    if usuario_actual["rol"] != ROLE_ENCARGADO:
        print("Acceso denegado: solo un Encargado puede registrar entregas.")
        return

    actualizar_estados_automaticos()

    solicitud_id = leer_entero("ID de solicitud: ")
    if solicitud_id is None:
        return

    solicitudes = cargar_json(REQUESTS_FILE)
    solicitud = _buscar_solicitud(solicitudes, solicitud_id)

    if solicitud is None:
        print("Solicitud no encontrada.")
        return

    if solicitud["estado"] != ESTADO_APROBADA:
        print("Solo se puede registrar la entrega de una solicitud Aprobada.")
        return

    solicitud["estado"] = ESTADO_ENTREGADA
    solicitud["entregada_en"] = datetime.now().isoformat(timespec="seconds")

    if guardar_json(REQUESTS_FILE, solicitudes):
        logging.info("Entrega registrada | solicitud=%s | por=%s", solicitud_id, usuario_actual["correo"])
        print("Entrega registrada. Estado actualizado a Entregada.")


def registrar_devolucion(usuario_actual: dict[str, Any]) -> None:
    """RN-08: se puede devolver desde Entregada o Atrasada."""
    if usuario_actual["rol"] != ROLE_ENCARGADO:
        print("Acceso denegado: solo un Encargado puede registrar devoluciones.")
        return

    actualizar_estados_automaticos()

    solicitud_id = leer_entero("ID de solicitud: ")
    if solicitud_id is None:
        return

    solicitudes = cargar_json(REQUESTS_FILE)
    solicitud = _buscar_solicitud(solicitudes, solicitud_id)

    if solicitud is None:
        print("Solicitud no encontrada.")
        return

    if solicitud["estado"] not in {ESTADO_ENTREGADA, ESTADO_ATRASADA}:
        print("Solo se puede registrar devolución de solicitudes Entregadas o Atrasadas.")
        return

    solicitud["estado"] = ESTADO_DEVUELTA
    solicitud["devuelta_en"] = datetime.now().isoformat(timespec="seconds")

    if guardar_json(REQUESTS_FILE, solicitudes):
        logging.info("Devolución registrada | solicitud=%s | por=%s", solicitud_id, usuario_actual["correo"])
        print("Devolución registrada. Estado actualizado a Devuelta.")


def consultar_prestamos_clasificados(usuario_actual: dict[str, Any]) -> None:
    actualizar_estados_automaticos()

    solicitudes = cargar_json(REQUESTS_FILE)
    hoy = date.today()

    if usuario_actual["rol"] == ROLE_SOLICITANTE:
        solicitudes = [s for s in solicitudes if s["solicitante"] == usuario_actual["correo"]]

    vigentes, futuros, atrasados = [], [], []

    for solicitud in solicitudes:
        fecha_inicio = date.fromisoformat(solicitud["fecha_inicio"])
        fecha_fin = date.fromisoformat(solicitud["fecha_fin"])

        if solicitud["estado"] == ESTADO_ATRASADA:
            atrasados.append(solicitud)
        elif solicitud["estado"] == ESTADO_ENTREGADA and fecha_inicio <= hoy <= fecha_fin:
            vigentes.append(solicitud)
        elif solicitud["estado"] == ESTADO_APROBADA and fecha_inicio > hoy:
            futuros.append(solicitud)

    print("\n--- PRÉSTAMOS VIGENTES ---")
    if vigentes:
        for s in vigentes:
            imprimir_solicitud(s)
    else:
        print("No existen préstamos vigentes.")

    print("\n--- PRÉSTAMOS FUTUROS ---")
    if futuros:
        for s in futuros:
            imprimir_solicitud(s)
    else:
        print("No existen préstamos futuros.")

    print("\n--- PRÉSTAMOS ATRASADOS ---")
    if atrasados:
        for s in atrasados:
            imprimir_solicitud(s)
    else:
        print("No existen préstamos atrasados.")


def crear_datos_demo() -> None:
    usuarios = cargar_json(USERS_FILE)

    if not usuarios:
        usuarios_demo = [
            {
                "nombre": "Encargado Uno",
                "rut": "11.111.111-1",
                "correo": "encargado1@demo.cl",
                "password_hash": hash_password("admin123"),
                "rol": ROLE_ENCARGADO,
                "activo": True,
            },
            {
                "nombre": "Encargado Dos",
                "rut": "22.222.222-2",
                "correo": "encargado2@demo.cl",
                "password_hash": hash_password("admin123"),
                "rol": ROLE_ENCARGADO,
                "activo": True,
            },
            {
                "nombre": "Solicitante Demo",
                "rut": "33.333.333-3",
                "correo": "solicitante@demo.cl",
                "password_hash": hash_password("user123"),
                "rol": ROLE_SOLICITANTE,
                "activo": True,
            },
        ]
        guardar_json(USERS_FILE, usuarios_demo)

    equipos = cargar_json(EQUIPMENT_FILE)

    if not equipos:
        equipos_demo = [
            {"id": "EQ-001", "nombre": "Notebook Lenovo", "descripcion": "Notebook de laboratorio", "activo": True},
            {"id": "EQ-002", "nombre": "Proyector Epson", "descripcion": "Proyector portátil", "activo": True},
            {"id": "EQ-003", "nombre": "Cámara Logitech", "descripcion": "Cámara USB", "activo": True},
        ]
        guardar_json(EQUIPMENT_FILE, equipos_demo)
