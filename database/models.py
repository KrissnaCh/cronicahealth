from dataclasses import dataclass, field
from datetime import date
from typing import Optional
import sqlite3

from database.crud import create_table_sql
from internal import Empty, InputWidgetType, SQLiteFieldConstraint, flags
import internal


@dataclass
class MedicalConsultation:
    """
    Modelo que representa una consulta médica general.
    """
    motivo_consulta: Optional[str] = flags(default=None,
                                           sqlite=SQLiteFieldConstraint.NONE,
                                           tcontrol=InputWidgetType.INPUT_TEXT,
                                           title="Motivo de Consulta",
                                           required=True)

    historia_enfermedad_actual: Optional[str] = flags(default=None,
                                                      sqlite=SQLiteFieldConstraint.NONE,
                                                      tcontrol=InputWidgetType.INPUT_TEXT,
                                                      title="Historial")

    examen_fisico: Optional[str] = flags(default=None,
                                         sqlite=SQLiteFieldConstraint.NONE,
                                         tcontrol=InputWidgetType.INPUT_TEXT,
                                         title="Examen Fisico")

    diagnostico: Optional[str] = flags(default=None,
                                       sqlite=SQLiteFieldConstraint.NONE,
                                       tcontrol=InputWidgetType.INPUT_TEXT,
                                       title="Diagnostico")

    plan_manejo: Optional[str] = flags(default=None,
                                       sqlite=SQLiteFieldConstraint.NONE,
                                       tcontrol=InputWidgetType.INPUT_TEXT,
                                       title="Plan de Manejo")

    seguimiento_fecha: Optional[date] = flags(default=None,
                                              sqlite=SQLiteFieldConstraint.NONE,
                                              tcontrol=InputWidgetType.DATE_PICKER,
                                              title="Fecha")

    seguimiento_observaciones: Optional[str] = flags(default=None,
                                                     sqlite=SQLiteFieldConstraint.NONE,
                                                     tcontrol=InputWidgetType.INPUT_TEXT,
                                                     title="Observaciones")


@dataclass
class InformacionGeneralPaciente:
    """
    Modelo que almacena la información general del paciente.
    """
    id: int = flags(default=0,
                    sqlite=SQLiteFieldConstraint.PRIMARY_KEY | SQLiteFieldConstraint.AUTOINCREMENT | SQLiteFieldConstraint.UNIQUE,
                    tcontrol=InputWidgetType.NONE,
                    title="Codigo",
                    readonly=True, showintable=False)

    nombre_completo: Optional[str] = flags(default=None,
                                           sqlite=SQLiteFieldConstraint.NONE,
                                           tcontrol=InputWidgetType.INPUT_TEXT,
                                           required=True,
                                           title="Nombre Completo", searchable=True)

    fecha_nacimiento: Optional[date] = flags(default=None,
                                             sqlite=SQLiteFieldConstraint.NONE,
                                             required=True,
                                             tcontrol=InputWidgetType.DATE_PICKER,
                                             title="Fecha de Nacimiento", showintable=False, searchable=True)

    edad: Optional[int] = flags(default=None,
                                sqlite=SQLiteFieldConstraint.NONE,
                                required=True,
                                tcontrol=InputWidgetType.INPUT_INT,
                                title="Edad", searchable=True)

    genero: Optional[str] = flags(default=None,
                                  sqlite=SQLiteFieldConstraint.NONE,
                                  tcontrol=InputWidgetType.COMBO,
                                  required=True,
                                  title="Genero",
                                  items=["Masculino", "Femenino"], searchable=True)

    cedula: Optional[str] = flags(default=None,
                                  sqlite=SQLiteFieldConstraint.NONE,
                                  required=True,
                                  tcontrol=InputWidgetType.INPUT_TEXT,
                                  title="Cedula", searchable=True)

    direccion: Optional[str] = flags(default=None, sqlite=SQLiteFieldConstraint.NONE,
                                     tcontrol=InputWidgetType.INPUT_TEXT,
                                     title="Direccion",
                                     required=False, showintable=False)

    telefono: Optional[str] = flags(default=None,
                                    sqlite=SQLiteFieldConstraint.NONE,
                                    tcontrol=InputWidgetType.INPUT_TEXT,
                                    title="Telefono",
                                    required=False)

    email: Optional[str] = flags(default=None,
                                 sqlite=SQLiteFieldConstraint.NONE,
                                 tcontrol=InputWidgetType.INPUT_TEXT,
                                 title="Email",
                                 required=False, showintable=False)

    estado_civil: Optional[str] = flags(default=None,
                                        sqlite=SQLiteFieldConstraint.NONE,
                                        tcontrol=InputWidgetType.COMBO,
                                        title="Estado Civil",
                                        items=[
                                            "Soltero",
                                            "Casado",
                                            "Divorciado",
                                            "Viudo",
                                            "Otro"], showintable=False)

    ocupacion: Optional[str] = flags(default=None,
                                     sqlite=SQLiteFieldConstraint.NONE,
                                     tcontrol=InputWidgetType.INPUT_TEXT,
                                     title="Ocupacion",
                                     required=False, showintable=False)


@dataclass
class AntecedentesPersonales:
    """
    Modelo que almacena los antecedentes personales del paciente.
    """
    id: int = flags(
        default=0,
        sqlite=SQLiteFieldConstraint.PRIMARY_KEY,
        tcontrol=InputWidgetType.NONE)
    """ID de referencia a Paciente"""
    
    patologicos: Optional[str] = flags(default=None,
                                       sqlite=SQLiteFieldConstraint.NONE,
                                       tcontrol=InputWidgetType.INPUT_TEXT,
                                       title="Patológicos")

    quirurgicos: Optional[str] = flags(default=None,
                                       sqlite=SQLiteFieldConstraint.NONE,
                                       tcontrol=InputWidgetType.INPUT_TEXT,
                                       title="Quirúrgicos")

    alergicos: Optional[str] = flags(default=None,
                                     sqlite=SQLiteFieldConstraint.NONE,
                                     tcontrol=InputWidgetType.INPUT_TEXT,
                                     title="Alergicos")

    traumaticos: Optional[str] = flags(default=None,
                                       sqlite=SQLiteFieldConstraint.NONE,
                                       tcontrol=InputWidgetType.INPUT_TEXT,
                                       title="Traumáticos")

    toxicos: Optional[str] = flags(default=None,
                                   sqlite=SQLiteFieldConstraint.NONE,
                                   tcontrol=InputWidgetType.INPUT_TEXT,
                                   title="Tóxicos")

    gineco_obstetricos: Optional[str] = flags(default=None,
                                              sqlite=SQLiteFieldConstraint.NONE,
                                              tcontrol=InputWidgetType.INPUT_TEXT,
                                              title="gineco-obstétricos")

    psiquiatricos: Optional[str] = flags(default=None,
                                         sqlite=SQLiteFieldConstraint.NONE,
                                         tcontrol=InputWidgetType.INPUT_TEXT,
                                         title="Psiquiátricos")

    hospitalizaciones_previas: Optional[str] = flags(default=None,
                                                     sqlite=SQLiteFieldConstraint.NONE,
                                                     tcontrol=InputWidgetType.INPUT_TEXT,
                                                     title="Hospitalizaciones Previas")


@dataclass
class AntecedentesFamiliares:
    """
    Modelo para antecedentes familiares.
    """
    """
    Modelo que almacena los antecedentes personales del paciente.
    """
    id: int = flags(
        default=0,
        sqlite=SQLiteFieldConstraint.PRIMARY_KEY,
        tcontrol=InputWidgetType.NONE)
    """ID de referencia a Paciente"""

    familiares: Optional[str] = flags(
        default=None,
        title="Informe:",
        sqlite=SQLiteFieldConstraint.NONE,
        tcontrol=InputWidgetType.INPUT_TEXT_RICH)


@dataclass
class ExamenFisicoPorSistemas:
    """
    Modelo de revisión de síntomas por sistemas.
    """
    id: int = flags(
        default=0,
        sqlite=SQLiteFieldConstraint.PRIMARY_KEY,
        tcontrol=InputWidgetType.NONE)
    """ID de referencia a Paciente"""

    general: Optional[str] = flags(default=None,
                                   sqlite=SQLiteFieldConstraint.NONE,
                                   tcontrol=InputWidgetType.INPUT_TEXT,
                                   title="General")

    neurologico: Optional[str] = flags(default=None,
                                       sqlite=SQLiteFieldConstraint.NONE,
                                       tcontrol=InputWidgetType.INPUT_TEXT,
                                       title="Neurologico")

    respiratorio: Optional[str] = flags(default=None,
                                        sqlite=SQLiteFieldConstraint.NONE,
                                        tcontrol=InputWidgetType.INPUT_TEXT,
                                        title="Respiratorio")

    cardiovascular: Optional[str] = flags(default=None,
                                          sqlite=SQLiteFieldConstraint.NONE,
                                          tcontrol=InputWidgetType.INPUT_TEXT,
                                          title="Cardiovascular")

    gastrointestinal: Optional[str] = flags(default=None,
                                            sqlite=SQLiteFieldConstraint.NONE,
                                            tcontrol=InputWidgetType.INPUT_TEXT,
                                            title="Gastrointestinal")

    genitourinario: Optional[str] = flags(default=None,
                                          sqlite=SQLiteFieldConstraint.NONE,
                                          tcontrol=InputWidgetType.INPUT_TEXT,
                                          title="Genitourinario")

    musculo_esqueletico: Optional[str] = flags(default=None,
                                               sqlite=SQLiteFieldConstraint.NONE,
                                               tcontrol=InputWidgetType.INPUT_TEXT,
                                               title="Musculo-esqueletico")

    dermatologico: Optional[str] = flags(default=None,
                                         sqlite=SQLiteFieldConstraint.NONE,
                                         tcontrol=InputWidgetType.INPUT_TEXT,
                                         title="Dermatologico")

    endocrino: Optional[str] = flags(default=None,
                                     sqlite=SQLiteFieldConstraint.NONE,
                                     tcontrol=InputWidgetType.INPUT_TEXT,
                                     title="Endocrino")

    psiquiatrico: Optional[str] = flags(default=None,
                                        sqlite=SQLiteFieldConstraint.NONE,
                                        tcontrol=InputWidgetType.INPUT_TEXT,
                                        title="Psiquiátrico")


@dataclass
class ExamenFisico:
    """
    Modelo para el examen físico general.
    """
     
    id: int = flags(
        default=0,
        sqlite=SQLiteFieldConstraint.PRIMARY_KEY,
        tcontrol=InputWidgetType.NONE)
    """ID de referencia a Paciente"""
    
    tension: Optional[str] = flags(default=None,
                                          sqlite=SQLiteFieldConstraint.NONE,
                                          tcontrol=InputWidgetType.INPUT_TEXT,
                                          title="Tension Arterial")
    
    frecuenciac: Optional[float] = flags(default=None,
                                  sqlite=SQLiteFieldConstraint.NONE,
                                  tcontrol=InputWidgetType.INPUT_FLOAT,
                                  title="Frecuencia Cardiaca")
    
    frecuenciar: Optional[float] = flags(default=None,
                                  sqlite=SQLiteFieldConstraint.NONE,
                                  tcontrol=InputWidgetType.INPUT_FLOAT,
                                  title="Frecuencia Respiratoria")
    
    temp: Optional[float] = flags(default=None,
                                  sqlite=SQLiteFieldConstraint.NONE,
                                  tcontrol=InputWidgetType.INPUT_FLOAT,
                                  title="Temperatura Corporal")
    
    satur: Optional[float] = flags(default=None,
                                  sqlite=SQLiteFieldConstraint.NONE,
                                  tcontrol=InputWidgetType.INPUT_FLOAT,
                                  title="Saturacion de Oxigeno")
    
    peso: Optional[float] = flags(default=None,
                                  sqlite=SQLiteFieldConstraint.NONE,
                                  tcontrol=InputWidgetType.INPUT_FLOAT,
                                  title="Peso")

    talla: Optional[float] = flags(default=None,
                                   sqlite=SQLiteFieldConstraint.NONE,
                                   tcontrol=InputWidgetType.INPUT_FLOAT,
                                   title="Talla")

    imc: Optional[float] = flags(default=None,
                                 sqlite=SQLiteFieldConstraint.NONE,
                                 tcontrol=InputWidgetType.INPUT_FLOAT,
                                 title="IMC")
    observaciones: Optional[str] = flags(default=None,
                                 sqlite=SQLiteFieldConstraint.NONE,
                                 tcontrol=InputWidgetType.INPUT_TEXT_RICH,
                                 title="Observaciones")


@dataclass
class PlanManejo:
    """
    Modelo para el plan de manejo clínico.
    """
    paraclinicos: Optional[str] = flags(default=None,
                                        sqlite=SQLiteFieldConstraint.NONE,
                                        tcontrol=InputWidgetType.INPUT_TEXT,
                                        title="")

    medicamentos: Optional[str] = flags(default=None,
                                        sqlite=SQLiteFieldConstraint.NONE,
                                        tcontrol=InputWidgetType.INPUT_TEXT,
                                        title="")

    recomendaciones: Optional[str] = flags(default=None,
                                           sqlite=SQLiteFieldConstraint.NONE,
                                           tcontrol=InputWidgetType.INPUT_TEXT,
                                           title="")

    remisiones: Optional[str] = flags(default=None,
                                      sqlite=SQLiteFieldConstraint.NONE,
                                      tcontrol=InputWidgetType.INPUT_TEXT,
                                      title="")


@dataclass
class Seguimiento:
    """
    Modelo para el seguimiento del paciente.
    """
    fecha_proximo_control: Optional[date] = flags(default=None,
                                                  sqlite=SQLiteFieldConstraint.NONE,
                                                  tcontrol=InputWidgetType.DATE_PICKER,
                                                  title="")

    observaciones_adicionales: Optional[str] = flags(default=None,
                                                     sqlite=SQLiteFieldConstraint.NONE,
                                                     tcontrol=InputWidgetType.INPUT_TEXT,
                                                     title="")


@dataclass
class Profesional:
    """
    Modelo que almacena los datos del profesional de la salud.
    """
    nombre: str = flags(default=None,
                        sqlite=SQLiteFieldConstraint.NONE,
                        tcontrol=InputWidgetType.INPUT_TEXT,
                        title="")
    numero_registro: str = flags(default=None,
                                 sqlite=SQLiteFieldConstraint.NONE,
                                 tcontrol=InputWidgetType.INPUT_TEXT,
                                 title="")
    especialidad: Optional[str] = flags(default=None,
                                        sqlite=SQLiteFieldConstraint.NONE,
                                        tcontrol=InputWidgetType.INPUT_TEXT,
                                        title="")
    firma_digital: Optional[str] = flags(default=None,
                                         sqlite=SQLiteFieldConstraint.NONE,
                                         tcontrol=InputWidgetType.INPUT_TEXT,
                                         title="")


@dataclass
class HistoriaClinica:
    """
    Modelo integral que agrupa toda la historia clínica de un paciente.
    """
    paciente: InformacionGeneralPaciente = field(
        default_factory=InformacionGeneralPaciente)
    motivo_consulta: str = Empty
    enfermedad_actual: str = Empty
    antecedentes_personales: AntecedentesPersonales = field(
        default_factory=AntecedentesPersonales)
    antecedentes_familiares: AntecedentesFamiliares = field(
        default_factory=AntecedentesFamiliares)
    examen_sistemas: ExamenFisicoPorSistemas = field(
        default_factory=ExamenFisicoPorSistemas)
    examen_fisico: ExamenFisico = field(default_factory=ExamenFisico)
    impresion_diagnostica: str = Empty
    plan_manejo: PlanManejo = field(default_factory=PlanManejo)
    seguimiento: Seguimiento = field(default_factory=Seguimiento)
    profesional: Profesional = field(default_factory=Profesional)
