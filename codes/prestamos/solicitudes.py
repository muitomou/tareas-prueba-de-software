from __future__ import annotations

import logging
from datetime import date, datetime
from typing import Any

from prestamos.config import (
    ESTADO_SOLICITADA,
    ESTADOS_QUE_BLOQUEAN_DISPONIBILIDAD,
    REQUESTS_FILE,
    ROLE_ENCARGADO,
)
from prestamos.equipos import buscar_equipo, listar_equipos
from prestamos.persistencia import (
    cargar_json,
    generar_id,
    guardar_json,
    leer_fecha,
    leer_no_vacio,
    periodos_se_superponen,
)


def equipo_disponible(
    equipo_id: str,
    fecha_inicio: date,
    fecha_fin: date,
    ignorar_solicitud_id: int | None = None,
) -> bool:
    """RN-04: un equipo está disponible si ninguna solicitud Aprobada,
    Entregada o Atrasada se superpone con el período consultado."""
    equipo = buscar_equipo(equipo_id)

    if equipo is None or not equipo.get("activo", True):
        return False

    solicitudes = cargar_json(REQUESTS_FILE)

    for solicitud in solicitudes:
        if ignorar_solicitud_id is not None and solicitud["id"] == ignorar_solicitud_id:
            continue

        if solicitud["estado"] not in ESTADOS_QUE_BLOQUEAN_DISPONIBILIDAD:
            continue

        if equipo_id not in solicitud["equipos"]:
            continue

        inicio_existente = date.fromisoformat(solicitud["fecha_inicio"])
        fin_existente = date.fromisoformat(solicitud["fecha_fin"])

        if periodos_se_superponen(fecha_inicio, fecha_fin, inicio_existente, fin_existente):
            return False

    return True


def crear_solicitud(usuario_actual: dict[str, Any]) -> None:
    """RN-03: crea una solicitud si todos los equipos pedidos están
    disponibles en el período especificado."""
    listar_equipos()

    entrada = leer_no_vacio("Ingrese los IDs de los equipos separados por coma: ")
    equipos_solicitados = [e.strip() for e in entrada.split(",") if e.strip()]

    if not equipos_solicitados:
        print("Debe seleccionar al menos un equipo.")
        return

    if len(set(equipos_solicitados)) != len(equipos_solicitados):
        print("No puede repetir el mismo equipo en una solicitud.")
        return

    for equipo_id in equipos_solicitados:
        equipo = buscar_equipo(equipo_id)

        if equipo is None:
            print(f"El equipo {equipo_id} no existe.")
            return

        if not equipo.get("activo", True):
            print(f"El equipo {equipo_id} se encuentra inactivo.")
            return

    fecha_inicio = leer_fecha("Fecha de inicio (YYYY-MM-DD): ")
    fecha_fin = leer_fecha("Fecha de devolución (YYYY-MM-DD): ")

    if fecha_inicio < date.today():
        print("La fecha de inicio no puede estar en el pasado.")
        return

    if fecha_fin < fecha_inicio:
        print("La fecha de devolución no puede ser anterior a la fecha de inicio.")
        return

    no_disponibles = [
        equipo_id
        for equipo_id in equipos_solicitados
        if not equipo_disponible(equipo_id, fecha_inicio, fecha_fin)
    ]

    if no_disponibles:
        print("No se puede realizar la solicitud. Equipos no disponibles: " + ", ".join(no_disponibles))
        return

    solicitudes = cargar_json(REQUESTS_FILE)

    nueva_solicitud = {
        "id": generar_id(solicitudes),
        "solicitante": usuario_actual["correo"],
        "equipos": equipos_solicitados,
        "fecha_inicio": fecha_inicio.isoformat(),
        "fecha_fin": fecha_fin.isoformat(),
        "estado": ESTADO_SOLICITADA,
        "creada_en": datetime.now().isoformat(timespec="seconds"),
        "aprobada_por": None,
        "rechazada_por": None,
        "motivo_rechazo": None,
        "entregada_en": None,
        "devuelta_en": None,
        "cancelada_en": None,
    }

    solicitudes.append(nueva_solicitud)

    if guardar_json(REQUESTS_FILE, solicitudes):
        logging.info(
            "Solicitud creada | id=%s | solicitante=%s | equipos=%s | periodo=%s/%s",
            nueva_solicitud["id"],
            usuario_actual["correo"],
            equipos_solicitados,
            fecha_inicio,
            fecha_fin,
        )
        print(f"Solicitud #{nueva_solicitud['id']} registrada en estado {ESTADO_SOLICITADA}.")


def imprimir_solicitud(solicitud: dict[str, Any]) -> None:
    print(
        f"ID: {solicitud['id']} | Solicitante: {solicitud['solicitante']} | "
        f"Equipos: {', '.join(solicitud['equipos'])} | "
        f"Periodo: {solicitud['fecha_inicio']} -> {solicitud['fecha_fin']} | "
        f"Estado: {solicitud['estado']}"
    )


def consultar_mis_solicitudes(usuario_actual: dict[str, Any]) -> None:
    solicitudes = cargar_json(REQUESTS_FILE)

    propias = [s for s in solicitudes if s["solicitante"] == usuario_actual["correo"]]

    if not propias:
        print("No posee solicitudes registradas.")
        return

    print("\n--- MIS SOLICITUDES ---")
    for solicitud in propias:
        imprimir_solicitud(solicitud)


def consultar_todas_solicitudes(usuario_actual: dict[str, Any]) -> None:
    if usuario_actual["rol"] != ROLE_ENCARGADO:
        print("Acceso denegado.")
        return

    solicitudes = cargar_json(REQUESTS_FILE)

    if not solicitudes:
        print("No existen solicitudes.")
        return

    print("\n--- TODAS LAS SOLICITUDES ---")
    for solicitud in solicitudes:
        imprimir_solicitud(solicitud)
