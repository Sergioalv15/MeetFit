from datetime import datetime, timezone, time
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
    String, Float, DateTime, Integer,
    ForeignKey, Boolean, Text, Time
)
from sqlalchemy.orm import relationship, mapped_column


db = SQLAlchemy()

# ==========================================================
# USUARIOS (ADMIN / TÉCNICOS)
# ==========================================================
class User(db.Model):
    __tablename__ = "user"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(120), nullable=False)
    email = mapped_column(String(120), unique=True, nullable=False)
    password_hash = mapped_column(String(200), nullable=False)

    role = mapped_column(String(50), default="admin")  

    active = mapped_column(Boolean, default=True)

    created_at = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )

    albaranes = relationship("Albaran", back_populates="tecnico")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "active": self.active,
            "created_at": self.created_at.isoformat()
        }


# ==========================================================
# CLIENTES
# ==========================================================
class Cliente(db.Model):
    __tablename__ = "cliente"

    id = mapped_column(Integer, primary_key=True)
    nombre_empresa = mapped_column(String(200), nullable=False)
    nif = mapped_column(String(50))
    direccion = mapped_column(String(200))
    cp = mapped_column(String(10))
    poblacion = mapped_column(String(100))
    telefono = mapped_column(String(50))
    persona_contacto = mapped_column(String(120))

    created_at = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )

    # Relaciones
    albaranes = relationship("Albaran", back_populates="cliente")

    def serialize(self):
        return {
            "id": self.id,
            "nombre_empresa": self.nombre_empresa,
            "nif": self.nif,
            "direccion": self.direccion,
            "cp": self.cp,
            "poblacion": self.poblacion,
            "telefono": self.telefono,
            "persona_contacto": self.persona_contacto
        }


# ==========================================================
# TARIFAS
# ==========================================================
class Tarifa(db.Model):
    __tablename__ = "tarifa"

    id = mapped_column(Integer, primary_key=True)
    nombre = mapped_column(String(120), nullable=False)
    precio_hora = mapped_column(Float, nullable=False)
    horas_jornada = mapped_column(Integer, default=8)
    precio_jornada = mapped_column(Float)

    activa = mapped_column(Boolean, default=True)

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "precio_hora": self.precio_hora,
            "horas_jornada": self.horas_jornada,
            "precio_jornada": self.precio_jornada,
            "activa": self.activa
        }


# ==========================================================
# ALBARÁN
# ==========================================================
class Albaran(db.Model):
    __tablename__ = "albaran"

    id = mapped_column(Integer, primary_key=True)

    cliente_id = mapped_column(
        Integer, ForeignKey("cliente.id"), nullable=False
    )
    tecnico_id = mapped_column(
        Integer, ForeignKey("user.id"), nullable=False
    )
    hora_inicio = mapped_column(Time, nullable=True)
    hora_fin = mapped_column(Time, nullable=True)
    fecha = mapped_column(DateTime, nullable=False)
    lugar_de_ensayo = mapped_column(String(200))

    horas_de_trabajo = mapped_column(Float, nullable=False)
    precio_hora = mapped_column(Float, nullable=False)

    precio_total = mapped_column(Float, nullable=False)

    descripcion = mapped_column(Text)

    created_at = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )

    # Relaciones
    cliente = relationship("Cliente", back_populates="albaranes")
    tecnico = relationship("User", back_populates="albaranes")

    def calcular_total(self):
        return round(self.horas_de_trabajo * self.precio_hora, 2)

    def serialize(self):
        return {
            "id": self.id,
            "cliente": self.cliente.serialize(),
            "tecnico": self.tecnico.serialize(),
            "fecha": self.fecha.isoformat(),
            "lugar_de_ensayo": self.lugar_de_ensayo,
            "horas_de_trabajo": self.horas_de_trabajo,
            "precio_hora": self.precio_hora,
            "precio_total": self.precio_total,
            "descripcion": self.descripcion
        }
