from __future__ import annotations

import hashlib
import json
import logging
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any


def cargar_json(archivo: Path) -> list[dict[str, Any]]:
    try:
        with archivo.open("r", encoding="utf-8") as f:
            datos = json.load(f)

        if not isinstance(datos, list):
            raise ValueError(f"El archivo {archivo.name} no contiene una lista JSON.")

        return datos

    except (OSError, json.JSONDecodeError, ValueError) as exc:
        logging.exception("Error al leer %s | %s", archivo.name, exc)
        return []


def guardar_json(archivo: Path, datos: list[dict[str, Any]]) -> bool:
    try:
        with archivo.open("w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)

        return True

    except OSError as exc:
        logging.exception("Error al guardar %s | %s", archivo.name, exc)
        print("No fue posible guardar la información.")
        return False


def generar_id(datos: list[dict[str, Any]]) -> int:
    if not datos:
        return 1

    return max(int(elemento["id"]) for elemento in datos) + 1


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def leer_no_vacio(mensaje: str) -> str:
    while True:
        valor = input(mensaje).strip()

        if valor:
            return valor

        print("Error: el campo no puede estar vacío.")


def leer_fecha(mensaje: str) -> date:
    while True:
        valor = input(mensaje).strip()

        try:
            return datetime.strptime(valor, "%Y-%m-%d").date()

        except ValueError:
            print("Fecha inválida. Utilice el formato YYYY-MM-DD.")


def leer_entero(mensaje: str) -> int | None:
    valor = input(mensaje).strip()

    try:
        return int(valor)

    except ValueError:
        print("Debe ingresar un número entero.")
        return None


def dias_habiles_entre(inicio: date, fin: date) -> int:
    """Cuenta días hábiles (lunes a viernes) en el rango (inicio, fin]."""
    if fin <= inicio:
        return 0

    dias = 0
    actual = inicio

    while actual < fin:
        actual += timedelta(days=1)

        if actual.weekday() < 5:
            dias += 1

    return dias


def periodos_se_superponen(
    inicio_a: date,
    fin_a: date,
    inicio_b: date,
    fin_b: date,
) -> bool:
    return inicio_a <= fin_b and inicio_b <= fin_a
