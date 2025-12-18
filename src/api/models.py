from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
    Integer,
    Float,
    String,
    Text,
    Date,
    Time,
    Boolean,
    ForeignKey
)
from sqlalchemy.orm import relationship, mapped_column

db = SQLAlchemy()

# ─────────────────────────────────────────────
# MODELO: Usuario
# ─────────────────────────────────────────────
class User(db.Model):
    __tablename__ = "user"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(120), nullable=False)
    email = mapped_column(String(120), unique=True, nullable=False)
    password_hash = mapped_column(String(255), nullable=False)

    is_admin = mapped_column(Boolean, default=False)

    albaranes = relationship("Albaran", back_populates="usuario")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "is_admin": self.is_admin
        }


# ─────────────────────────────────────────────
# MODELO: Cliente
# ─────────────────────────────────────────────
class Cliente(db.Model):
    __tablename__ = "cliente"

    id = mapped_column(Integer, primary_key=True)
    nombre_empresa = mapped_column(String(200), nullable=False)

    tarifas = relationship("TarifaCliente", back_populates="cliente")
    albaranes = relationship("Albaran", back_populates="cliente")

    def serialize(self):
        return {
            "id": self.id,
            "nombre_empresa": self.nombre_empresa
        }


# ─────────────────────────────────────────────
# MODELO: Tarifa por Cliente
# ─────────────────────────────────────────────
class TarifaCliente(db.Model):
    __tablename__ = "tarifa_cliente"

    id = mapped_column(Integer, primary_key=True)

    cliente_id = mapped_column(
        Integer, ForeignKey("cliente.id"), nullable=False
    )

    ensayo = mapped_column(
        String(150), nullable=False
    )  # ej: "Líquidos penetrantes"

    modalidad = mapped_column(
        String(20), nullable=False
    )  # "horas" | "jornada"

    precio_tecnico = mapped_column(Float, nullable=False)
    precio_ayudante = mapped_column(Float, nullable=False)

    horas_minimas = mapped_column(Float, default=1)

    activa = mapped_column(Boolean, default=True)

    cliente = relationship("Cliente", back_populates="tarifas")

    def serialize(self):
        return {
            "id": self.id,
            "cliente_id": self.cliente_id,
            "ensayo": self.ensayo,
            "modalidad": self.modalidad,
            "horas_minimas": self.horas_minimas,
            "activa": self.activa
        }


# ─────────────────────────────────────────────
# MODELO: Albarán
# ─────────────────────────────────────────────
class Albaran(db.Model):
    __tablename__ = "albaran"

    id = mapped_column(Integer, primary_key=True)

    # Relaciones
    cliente_id = mapped_column(Integer, ForeignKey("cliente.id"), nullable=False)
    usuario_id = mapped_column(Integer, ForeignKey("user.id"), nullable=False)

    cliente = relationship("Cliente", back_populates="albaranes")
    usuario = relationship("User", back_populates="albaranes")

    # Datos generales
    fecha = mapped_column(Date, nullable=False)
    hora_inicio = mapped_column(Time, nullable=True)
    hora_fin = mapped_column(Time, nullable=True)

    lugar_de_ensayo = mapped_column(Text, nullable=True)
    persona_contacto = mapped_column(Text, nullable=True)

    # Líneas de trabajo (texto final ya procesado)
    linea_trabajo_1 = mapped_column(Text, nullable=False)
    linea_trabajo_2 = mapped_column(Text, nullable=True)
    linea_trabajo_3 = mapped_column(Text, nullable=True)

    # Total final (único importe visible)
    total_general = mapped_column(Float, nullable=False)

    # Notas / descripciones opcionales
    descripcion_linea_1 = mapped_column(Text, nullable=True)
    descripcion_linea_2 = mapped_column(Text, nullable=True)
    descripcion_linea_3 = mapped_column(Text, nullable=True)
    descripcion_linea_4 = mapped_column(Text, nullable=True)

    created_at = mapped_column(Date, default=datetime.utcnow)

    def serialize(self):
        return {
            "id": self.id,
            "fecha": self.fecha.isoformat(),
            "cliente": self.cliente.serialize(),
            "total_general": self.total_general,
            "lineas": [
                self.linea_trabajo_1,
                self.linea_trabajo_2,
                self.linea_trabajo_3
            ]
        }
