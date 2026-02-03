from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, EmailStr, field_validator, ValidationError
from typing import Optional, List
from datetime import date
import re

# Importamos funciones de base de datos
from app.database import (
    fetch_all_reservas,
    insert_reserva,
    delete_reserva,
    fetch_reserva_by_id,
    update_reserva
)

# --------------------------------------------------
# MODELOS Pydantic
# --------------------------------------------------

# Modelo base con validaciones comunes
class ReservaBase(BaseModel):
    nombre_cliente: str
    email: EmailStr
    telefono: str
    destino: str
    fecha_salida: date
    fecha_regreso: date
    num_personas: int
    tipo_paquete: str
    tipo_viaje: str
    forma_pago: str

    @field_validator("nombre_cliente", "telefono", "destino")
    @classmethod
    def validar_texto(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("El campo no puede estar vacío")
        return v.strip()

    @field_validator("num_personas")
    @classmethod
    def validar_personas(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("Debe haber al menos una persona")
        return v

    @field_validator("fecha_regreso")
    @classmethod
    def validar_fechas(cls, v: date, info):
        fecha_salida = info.data.get("fecha_salida")
        if fecha_salida and v <= fecha_salida:
            raise ValueError("La fecha de regreso debe ser posterior a la de salida")
        return v

    @field_validator("tipo_paquete")
    @classmethod
    def validar_paquete(cls, v: str) -> str:
        if v not in ["economico", "estandar", "lujo"]:
            raise ValueError("Tipo de paquete no válido")
        return v

    @field_validator("tipo_viaje")
    @classmethod
    def validar_viaje(cls, v: str) -> str:
        if v not in ["ocio", "familiar", "aventura", "naturaleza", "gastronomico", "cultural"]:
            raise ValueError("Tipo de viaje no válido")
        return v

    @field_validator("forma_pago")
    @classmethod
    def validar_pago(cls, v: str) -> str:
        if v not in ["pago_unico", "a_plazos"]:
            raise ValueError("Forma de pago no válida")
        return v


class ReservaDB(ReservaBase):
    id: int


class ReservaCreate(ReservaBase):
    pass


class ReservaUpdate(ReservaBase):
    pass


# --------------------------------------------------
# APP
# --------------------------------------------------

app = FastAPI(title="GoTrip – Agencia de Viajes")

# Servir archivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Motor de plantillas
templates = Jinja2Templates(directory="app/templates")


# --------------------------------------------------
# UTILIDAD
# --------------------------------------------------
def map_rows_to_reservas(rows: List[dict]) -> List[ReservaDB]:
    """
    Convierte las filas del SELECT * FROM reservas (dict) 
    en objetos ReservaDB (sin validaciones estrictas para datos existentes).
    """
    return [ReservaDB(**row) for row in rows]


# --------------------------------------------------
# RUTAS
# --------------------------------------------------

# --- GET principal ---
@app.get("/", response_class=HTMLResponse)
def get_index(request: Request, msg: str = None):
    # 1️⃣ Obtenemos los datos desde MySQL
    rows = fetch_all_reservas()

    # 2️⃣ Convertimos cada fila a Producto (valida estructura)
    reservas = map_rows_to_reservas(rows)

    # Lógica para decidir qué mensaje mostrar
    mensaje_exito = None
    if msg == "success":
        mensaje_exito = "¡Reserva creada con éxito!"
    elif msg == "updated":
        mensaje_exito = "¡Reserva actualizada correctamente!"
    elif msg == "deleted":
        mensaje_exito = "La reserva ha sido eliminada."

    # 3️⃣ Enviamos a la plantilla
    return templates.TemplateResponse(
        "pages/index.html",
        {
            "request": request,
            "reservas": reservas,
            "mensaje_exito": mensaje_exito,
            "msg": msg
        }
        
    )


# --- GET formulario nueva reserva---
@app.get("/reservas/nueva", response_class=HTMLResponse)
def get_nueva_reserva(request: Request):
    return templates.TemplateResponse(
        "pages/nueva_reserva.html",
        {"request": request}
    )


# --- POST guardar nueva reserva ---
@app.post("/reservas/nueva")
def post_nueva_reserva(
    request: Request,
    nombre_cliente: str = Form(...),
    email: EmailStr = Form(...),
    telefono: str = Form(...),
    destino: str = Form(...),
    fecha_salida: date = Form(...),
    fecha_regreso: date = Form(...),
    num_personas: int = Form(...),
    tipo_paquete: str = Form(...),
    tipo_viaje: str = Form(...),
    forma_pago: str = Form(...)
):
    try:
        # 1. Validamos los datos con Pydantic
        reserva = ReservaCreate(
            nombre_cliente=nombre_cliente,
            email=email,
            telefono=telefono,
            destino=destino,
            fecha_salida=fecha_salida,
            fecha_regreso=fecha_regreso,
            num_personas=num_personas,
            tipo_paquete=tipo_paquete,
            tipo_viaje=tipo_viaje,
            forma_pago=forma_pago
        )

        # 2. Insertamos en la base de datos MySQL
        insert_reserva(**reserva.model_dump())
        
        # 3. ÉXITO: Redirigimos al inicio con el parámetro de éxito en la URL
        return RedirectResponse(url="/?msg=success", status_code=303)

    except ValidationError as e:
        # ERROR: Si Pydantic detecta fallos, volvemos al formulario con la lista de errores
        errores = [err["msg"] for err in e.errors()]
        return templates.TemplateResponse(
            "pages/nueva_reserva.html",
            {
                "request": request,
                "errores": errores
            },
            status_code=422
        )

# --- DELETE eliminar reserva ---
@app.delete("/reservas/{reserva_id}")
def delete_reserva_endpoint(reserva_id: int):
    if not delete_reserva(reserva_id):
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return JSONResponse({"mensaje": "Reserva eliminada"})


# --- GET formulario editar reserva ---
@app.get("/reservas/editar/{reserva_id}", response_class=HTMLResponse)
def get_editar_reserva(request: Request, reserva_id: int):
    """
    Endpoint para mostrar el formulario de edición con datos precargados.
    """
    # Obtenemos los datos del producto
    data = fetch_reserva_by_id(reserva_id)
    if not data:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    
    # Convertimos a modelo ProductoDB para mostrar en formulario (sin validaciones)
    reserva = ReservaDB(**data)
    return templates.TemplateResponse(
        "pages/editar_reserva.html",
        {"request": request, "reserva": reserva}
    )


# --- POST actualizar reserva a través de su id ---
@app.post("/reservas/editar/{reserva_id}")
def post_editar_reserva(
    request: Request,
    reserva_id: int,
    nombre_cliente: str = Form(...),
    email: EmailStr = Form(...),
    telefono: str = Form(...),
    destino: str = Form(...),
    fecha_salida: date = Form(...),
    fecha_regreso: date = Form(...),
    num_personas: int = Form(...),
    tipo_paquete: str = Form(...),
    tipo_viaje: str = Form(...),
    forma_pago: str = Form(...)
):
    try:
        reserva = ReservaUpdate(
            nombre_cliente=nombre_cliente,
            email=email,
            telefono=telefono,
            destino=destino,
            fecha_salida=fecha_salida,
            fecha_regreso=fecha_regreso,
            num_personas=num_personas,
            tipo_paquete=tipo_paquete,
            tipo_viaje=tipo_viaje,
            forma_pago=forma_pago
        )

        if not update_reserva(reserva_id, **reserva.model_dump()):
            raise HTTPException(status_code=404, detail="Reserva no encontrada")

        return RedirectResponse(url="/?msg=updated", status_code=303)

    except ValidationError as e:
        errores = [err["msg"] for err in e.errors()]
        reserva_temp = ReservaDB(id=reserva_id, **reserva.model_dump())
        return templates.TemplateResponse(
            "pages/editar_reserva.html",
            {
                "request": request,
                "reserva": reserva_temp,
                "errores": errores
            },
            status_code=422
        )
    
    except Exception as e:
        # Error crítico (Base de datos, servidor, etc.)
        print(f"Error inesperado: {e}") # Para que tú lo veas en la consola
        return RedirectResponse(url="/?msg=error", status_code=303)