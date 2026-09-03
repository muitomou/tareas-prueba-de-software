from __future__ import annotations

import logging
import os
from pathlib import Path

import sentry_sdk

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"

USERS_FILE = DATA_DIR / "usuarios.json"
EQUIPMENT_FILE = DATA_DIR / "equipos.json"
REQUESTS_FILE = DATA_DIR / "solicitudes.json"
LOG_FILE = LOG_DIR / "app.log"

ROLE_SOLICITANTE = "Solicitante"
ROLE_ENCARGADO = "Encargado"

ESTADO_SOLICITADA = "Solicitada"
ESTADO_APROBADA = "Aprobada"
ESTADO_RECHAZADA = "Rechazada"
ESTADO_ENTREGADA = "Entregada"
ESTADO_DEVUELTA = "Devuelta"
ESTADO_ATRASADA = "Atrasada"
ESTADO_CANCELADA = "Cancelada"
ESTADO_VENCIDA = "Vencida"

ESTADOS_QUE_BLOQUEAN_DISPONIBILIDAD = {
    ESTADO_APROBADA,
    ESTADO_ENTREGADA,
    ESTADO_ATRASADA,
}

ESTADOS_CANCELABLES = {
    ESTADO_SOLICITADA,
    ESTADO_APROBADA,
}

DIAS_HABILES_LIMITE_VENCIMIENTO = 5


def configurar_directorios() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    LOG_DIR.mkdir(exist_ok=True)

    for archivo in (USERS_FILE, EQUIPMENT_FILE, REQUESTS_FILE):
        if not archivo.exists():
            archivo.write_text("[]\n", encoding="utf-8")


def configurar_logging() -> None:
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        encoding="utf-8",
    )


def configurar_sentry() -> None:
    """El DSN se entrega mediante la variable de entorno SENTRY_DSN
    y nunca debe quedar escrito en el código ni en el repositorio."""
    dsn = os.getenv("SENTRY_DSN", "").strip()

    if not dsn:
        logging.warning("Sentry no fue inicializado porque SENTRY_DSN no está configurado.")
        return

    sentry_sdk.init(
        dsn=dsn,
        send_default_pii=False,
        traces_sample_rate=0.0,
        environment="development",
    )

    logging.info("Sentry inicializado correctamente.")


def registrar_excepcion(exc: Exception, contexto: str) -> None:
    logging.exception("%s | %s", contexto, exc)

    try:
        sentry_sdk.capture_exception(exc)
    except Exception as sentry_error:
        logging.error("No se pudo enviar la excepción a Sentry | %s", sentry_error)
