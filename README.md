<<<<<<< HEAD
# Sistema de Préstamo de Equipos

Aplicación de línea de comandos desarrollada en Python para administrar
préstamos de equipos tecnológicos de un laboratorio universitario.

> Tarea 1 

## Tecnologías

- Python 3.10 o superior
- JSON para persistencia local (sin base de datos)
- `logging` para generación de logs locales
- `sentry-sdk` para monitoreo de errores mediante Sentry.io

## Estructura del proyecto

```text
codes/
├── app.py                 # Punto de entrada de la aplicación
├── requirements.txt
├── .env.example
├── prestamos/
│   ├── config.py          # Rutas, constantes de estado/rol, logging y Sentry
│   ├── persistencia.py    # Lectura/escritura JSON y utilidades comunes
│   ├── usuarios.py        # Registro, login y roles (RN-01, RN-02)
│   ├── equipos.py         # Registro y consulta de equipos
│   ├── solicitudes.py     # Disponibilidad, creación, aprobación, rechazo y cancelación
│   ├── operaciones.py     # Entregas, devoluciones, consultas clasificadas y datos demo
│   └── cli.py             # Menús por rol y punto de entrada principal
├── data/                  # Persistencia local (generada en tiempo de ejecución)
└── logs/                  # app.log (generado en tiempo de ejecución)
```

## Instalación

```bash
git clone <URL_DEL_REPOSITORIO>
cd sistema-prestamo-equipos/codes
pip install -r requirements.txt
cp .env.example .env   # completar SENTRY_DSN si se desea monitoreo
```

## Configuración de Sentry

Crear un proyecto Python en [Sentry.io](https://sentry.io/welcome/) y obtener el DSN.

En PowerShell:

```powershell
$env:SENTRY_DSN="TU_DSN"
```

En Linux/macOS:

```bash
export SENTRY_DSN="TU_DSN"
```

El DSN no debe escribirse directamente en el código ni subirse al repositorio.
Si la variable no está definida, la aplicación funciona igualmente y solo
registra una advertencia en el log local.

## Ejecución

```bash
python app.py
```

Los datos de demostración (usuarios y equipos) se crean automáticamente en
el primer arranque si `data/` se encuentra vacío.

## Datos de demostración

| Usuario | Correo | Contraseña | Rol |
| --- | --- | --- | --- |
| Encargado Uno | encargado1@demo.cl | admin123 | Encargado |
| Encargado Dos | encargado2@demo.cl | admin123 | Encargado |
| Solicitante Demo | solicitante@demo.cl | user123 | Solicitante |

## Reglas de negocio implementadas

- RN-01: solo un Encargado administra y registra usuarios.
- RN-02: solo usuarios registrados y activos pueden iniciar sesión.
- RN-03: las solicitudes requieren equipos disponibles y un período.
- RN-04: disponibilidad considerando solicitudes Aprobadas, Entregadas o Atrasadas que se superpongan.
- RN-05: solo Encargados pueden aprobar o rechazar.
- RN-06: todo rechazo requiere justificación.
- RN-07: solicitudes no resueltas durante más de 5 días hábiles pasan a Vencida; cancelación solo desde Solicitada o Aprobada.
- RN-08: flujo Aprobada -> Entregada -> Devuelta o Atrasada -> Devuelta.
- RN-09: un Encargado no puede aprobar ni rechazar su propia solicitud.
- RN-10: un usuario con préstamo Atrasado no puede obtener aprobación de nuevas solicitudes.

## Persistencia

```text
codes/data/usuarios.json
codes/data/equipos.json
codes/data/solicitudes.json
```

## Logs

```text
codes/logs/app.log
```

## Autores

- Diego Espinoza
- Mauro Castillo

## Licencia

MIT. Ver [LICENSE](LICENSE).
=======
# tareas-prueba-de-software
>>>>>>> origin/develop
