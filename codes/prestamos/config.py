from __future__ import annotations

from pathlib import Path

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
