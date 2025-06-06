from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime

Base = declarative_base()

class Paciente(Base):
    __tablename__ = "pacientes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String)
    telefono = Column(String, unique=True)
    fecha_nacimiento = Column(String)
    historial = Column(Text)
    conversaciones = relationship("Conversacion", back_populates="paciente")
    citas = relationship("Cita", back_populates="paciente")

class Cita(Base):
    __tablename__ = "citas"
    id = Column(Integer, primary_key=True, autoincrement=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    fecha = Column(String)
    hora = Column(String)
    especialista = Column(String)
    confirmada = Column(Boolean, default=False)
    paciente = relationship("Paciente", back_populates="citas")

class Conversacion(Base):
    __tablename__ = "conversaciones"
    id = Column(Integer, primary_key=True, autoincrement=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    mensaje = Column(Text)
    respuesta = Column(Text)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    paciente = relationship("Paciente", back_populates="conversaciones")

# Configuración de la base de datos
engine = create_engine("sqlite:///asistente_memoria.db")
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)
