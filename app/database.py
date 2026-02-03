from dotenv import load_dotenv, find_dotenv
import os
import mysql.connector
from typing import List, Dict, Any, cast
from mysql.connector.cursor import MySQLCursorDict  

# Carga .env desde la raíz
load_dotenv(find_dotenv())


# --------------------------------------------------
# CONEXIÓN
# --------------------------------------------------

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),        
        user=os.getenv("DB_USER", "user_gotrip"),
        password=os.getenv("DB_PASSWORD", "gotrip123"),
        database=os.getenv("DB_NAME", "go_trip"),
        port=int(os.getenv("DB_PORT", "3306")),
        charset="utf8mb4"
    )

# --------------------------------------------------
# SELECT: listar todas las reservas
# --------------------------------------------------
def fetch_all_reservas() -> List[Dict[str, Any]]:
    """
    Obtiene todas las reservas.
    """
    conn = None
    try:
        conn = get_connection()
        cur: MySQLCursorDict
        cur = conn.cursor(dictionary=True)  # type: ignore[assignment]
        try:
            cur.execute("SELECT * FROM reservas ORDER BY fecha_salida")
            rows = cast(List[Dict[str, Any]], cur.fetchall())
            return rows
        finally:
            cur.close()
    finally:
        if conn:
            conn.close()

# --------------------------------------------------
# INSERT: nueva reserva
# --------------------------------------------------
def insert_reserva(
    nombre_cliente: str,
    email: str,
    telefono: str,
    destino: str,
    fecha_salida: str,
    fecha_regreso: str,
    num_personas: int,
    tipo_paquete: str,
    tipo_viaje: str,
    forma_pago: str
) -> int:
    """
    Inserta una nueva reserva y devuelve su ID.
    """
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                """
                INSERT INTO reservas
                (nombre_cliente, email, telefono, destino, fecha_salida, fecha_regreso,
                 num_personas, tipo_paquete, tipo_viaje, forma_pago)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    nombre_cliente, email, telefono, destino,
                    fecha_salida, fecha_regreso, num_personas,
                    tipo_paquete, tipo_viaje, forma_pago
                )
            )
            conn.commit()
            return cur.lastrowid or 0
        finally:
            cur.close()
    finally:
        if conn:
            conn.close()

# --------------------------------------------------
# SELECT: obtener reserva por ID
# --------------------------------------------------
def fetch_reserva_by_id(reserva_id: int) -> Dict[str, Any] | None:
    """
    Obtiene una reserva por su ID.
    Retorna un dict con los datos del producto o None si no existe.
    """
    conn = None
    try:
        conn = get_connection()
        cur: MySQLCursorDict
        cur = conn.cursor(dictionary=True)  # type: ignore[assignment]
        try:
            cur.execute(
                "SELECT * FROM reservas WHERE id = %s",
                (reserva_id,)
            )
            result = cur.fetchone()
            return dict(result) if result else None
        finally:
            cur.close()
    finally:
        if conn:
            conn.close()


# --------------------------------------------------
# DELETE: eliminar reserva
# --------------------------------------------------
def delete_reserva(reserva_id: int) -> bool:
    """
    Elimina una reserva de la base de datos por su ID.
    Retorna True si se eliminó correctamente, False si no se encontró.
    """
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                "DELETE FROM reservas WHERE id = %s",
                (reserva_id,)
            )
            conn.commit()
            return cur.rowcount > 0
        finally:
            cur.close()
    finally:
        if conn:
            conn.close()


# --------------------------------------------------
# UPDATE: actualizar reserva
# --------------------------------------------------
def update_reserva(
    reserva_id: int,
    nombre_cliente: str,
    email: str,
    telefono: str,
    destino: str,
    fecha_salida: str,
    fecha_regreso: str,
    num_personas: int,
    tipo_paquete: str,
    tipo_viaje: str,
    forma_pago: str
) -> bool:
    """
    Actualiza los datos de una reserva existente.
    Retorna True si se actualizó correctamente, False si no se encontró.
    """
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                """
                UPDATE reservas
                SET nombre_cliente = %s,
                    email = %s,
                    telefono = %s,
                    destino = %s,
                    fecha_salida = %s,
                    fecha_regreso = %s,
                    num_personas = %s,
                    tipo_paquete = %s,
                    tipo_viaje = %s,
                    forma_pago = %s
                WHERE id = %s
                """,
                (
                    nombre_cliente, email, telefono, destino,
                    fecha_salida, fecha_regreso, num_personas,
                    tipo_paquete, tipo_viaje, forma_pago,
                    reserva_id
                )
            )
            conn.commit()
            return cur.rowcount > 0
        finally:
            cur.close()
    finally:
        if conn:
            conn.close()