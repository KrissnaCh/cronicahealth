from dataclasses import dataclass, field
from datetime import date
from enum import auto
from typing import Optional
import sqlite3

from database.crud import create_table_sql
from internal import Empty, InputWidgetType, SQLiteFieldConstraint, flags, flagsv2
import internal


@dataclass
class MedicalConsultation:
    """
    Modelo que representa una consulta médica general.
    """

    motivo_consulta: Optional[str] = flags(
        default=None,
        sqlite=SQLiteFieldConstraint.NONE,
        tcontrol=InputWidgetType.INPUT_TEXT,
        title="Motivo de Consulta",
        required=True,
    )

    historia_enfermedad_actual: Optional[str] = flags(
        default=None,
        sqlite=SQLiteFieldConstraint.NONE,
        tcontrol=InputWidgetType.INPUT_TEXT,
        title="Historial",
    )

    examen_fisico: Optional[str] = flags(
        default=None,
        sqlite=SQLiteFieldConstraint.NONE,
        tcontrol=InputWidgetType.INPUT_TEXT,
        title="Examen Fisico",
    )

    diagnostico: Optional[str] = flags(
        default=None,
        sqlite=SQLiteFieldConstraint.NONE,
        tcontrol=InputWidgetType.INPUT_TEXT,
        title="Diagnostico",
    )

    plan_manejo: Optional[str] = flags(
        default=None,
        sqlite=SQLiteFieldConstraint.NONE,
        tcontrol=InputWidgetType.INPUT_TEXT,
        title="Plan de Manejo",
    )

    seguimiento_fecha: Optional[date] = flags(
        default=None,
        sqlite=SQLiteFieldConstraint.NONE,
        tcontrol=InputWidgetType.DATE_PICKER,
        title="Fecha",
    )

    seguimiento_observaciones: Optional[str] = flags(
        default=None,
        sqlite=SQLiteFieldConstraint.NONE,
        tcontrol=InputWidgetType.INPUT_TEXT,
        title="Observaciones",
    )


@dataclass
class Seguimiento:
    """
    Modelo para el seguimiento del paciente.
    """

    fecha_proximo_control: Optional[date] = flags(
        default=None,
        sqlite=SQLiteFieldConstraint.NONE,
        tcontrol=InputWidgetType.DATE_PICKER,
        title="Fecha Prox. Control",
    )

    observaciones_adicionales: Optional[str] = flags(
        default=None,
        sqlite=SQLiteFieldConstraint.NONE,
        tcontrol=InputWidgetType.INPUT_TEXT_RICH,
        title="Observaciones",
    )


@dataclass
class PlanManejo:
    """
    Modelo para el plan de manejo clínico.
    """

    paraclinicos: Optional[str] = flags(
        default=None,
        sqlite=SQLiteFieldConstraint.NONE,
        tcontrol=InputWidgetType.INPUT_TEXT,
        title="Paraclínicos",
    )

    medicamentos: Optional[str] = flags(
        default=None,
        sqlite=SQLiteFieldConstraint.NONE,
        tcontrol=InputWidgetType.INPUT_TEXT,
        title="Medicamentos",
    )

    recomendaciones: Optional[str] = flags(
        default=None,
        sqlite=SQLiteFieldConstraint.NONE,
        tcontrol=InputWidgetType.INPUT_TEXT,
        title="Recomendaciones",
    )

    remisiones: Optional[str] = flags(
        default=None,
        sqlite=SQLiteFieldConstraint.NONE,
        tcontrol=InputWidgetType.INPUT_TEXT,
        title="Remisiones",
    )


@dataclass
class InformacionGeneralPaciente:
    """
    Modelo que almacena la información general del paciente.
    """

    id: int = flags(
        default=0,
        sqlite=SQLiteFieldConstraint.PRIMARY_KEY
        | SQLiteFieldConstraint.AUTOINCREMENT
        | SQLiteFieldConstraint.UNIQUE,
        tcontrol=InputWidgetType.NONE,
        title="Codigo",
        readonly=True,
        showintable=False,
    )
    lb_g: int = flags(
        default=0,
        sqlite=SQLiteFieldConstraint.IGNORE,
        tcontrol=InputWidgetType.SEP,
        title="Informacion General",
        required=False,
        showintable=False,
    )
    nombre_completo: Optional[str] = flags(
        default=None,
        sqlite=SQLiteFieldConstraint.NONE,
        tcontrol=InputWidgetType.INPUT_TEXT,
        required=True,
        title="Nombre Completo",
        searchable=True,
    )

    fecha_nacimiento: Optional[date] = flags(
        default=None,
        sqlite=SQLiteFieldConstraint.NONE,
        required=True,
        tcontrol=InputWidgetType.DATE_PICKER,
        title="Fecha de Nacimiento",
        showintable=False,
        searchable=True,
    )

    edad: Optional[int] = flags(
        default=None,
        sqlite=SQLiteFieldConstraint.NONE,
        required=True,
        tcontrol=InputWidgetType.INPUT_INT,
        title="Edad",
        searchable=True,
    )

    genero: Optional[str] = flags(
        default=None,
        sqlite=SQLiteFieldConstraint.NONE,
        tcontrol=InputWidgetType.COMBO,
        required=True,
        title="Genero",
        items=["Masculino", "Femenino"],
        searchable=True,
    )

    cedula: Optional[str] = flags(
        default=None,
        sqlite=SQLiteFieldConstraint.NONE,
        required=True,
        tcontrol=InputWidgetType.INPUT_TEXT,
        title="Cedula",
        searchable=True,
    )

    direccion: Optional[str] = flags(
        default=None,
        sqlite=SQLiteFieldConstraint.NONE,
        tcontrol=InputWidgetType.INPUT_TEXT,
        title="Direccion",
        required=False,
        showintable=False,
    )

    telefono: Optional[str] = flags(
        default=None,
        sqlite=SQLiteFieldConstraint.NONE,
        tcontrol=InputWidgetType.INPUT_TEXT,
        title="Telefono",
        required=False,
    )

    email: Optional[str] = flags(
        default=None,
        sqlite=SQLiteFieldConstraint.NONE,
        tcontrol=InputWidgetType.INPUT_TEXT,
        title="Email",
        required=False,
        showintable=False,
    )

    estado_civil: Optional[str] = flags(
        default=None,
        sqlite=SQLiteFieldConstraint.NONE,
        tcontrol=InputWidgetType.COMBO,
        title="Estado Civil",
        items=["Soltero", "Casado", "Divorciado", "Viudo", "Otro"],
        showintable=False,
    )

    ocupacion: Optional[str] = flags(
        default=None,
        sqlite=SQLiteFieldConstraint.NONE,
        tcontrol=InputWidgetType.INPUT_TEXT,
        title="Ocupacion",
        required=False,
        showintable=False,
    )

    lb_ap: int = flags(
        default=0,
        sqlite=SQLiteFieldConstraint.IGNORE,
        tcontrol=InputWidgetType.SEP,
        title="Antecedentes Personales",
        required=False,
        showintable=False,
    )

    patologicos: Optional[str] = flags(
        default=None,
        sqlite=SQLiteFieldConstraint.NONE,
        tcontrol=InputWidgetType.INPUT_TEXT,
        title="Patológicos",
        showintable=False,
    )

    quirurgicos: Optional[str] = flags(
        default=None,
        sqlite=SQLiteFieldConstraint.NONE,
        tcontrol=InputWidgetType.INPUT_TEXT,
        title="Quirúrgicos",
        showintable=False,
    )

    alergicos: Optional[str] = flags(
        default=None,
        sqlite=SQLiteFieldConstraint.NONE,
        tcontrol=InputWidgetType.INPUT_TEXT,
        title="Alergicos",
        showintable=False,
    )

    traumaticos: Optional[str] = flags(
        default=None,
        sqlite=SQLiteFieldConstraint.NONE,
        tcontrol=InputWidgetType.INPUT_TEXT,
        title="Traumáticos",
        showintable=False,
    )

    toxicos: Optional[str] = flags(
        default=None,
        sqlite=SQLiteFieldConstraint.NONE,
        tcontrol=InputWidgetType.INPUT_TEXT,
        title="Tóxicos",
        showintable=False,
    )

    gineco_obstetricos: Optional[str] = flags(
        default=None,
        sqlite=SQLiteFieldConstraint.NONE,
        tcontrol=InputWidgetType.INPUT_TEXT,
        title="gineco-obstétricos",
        showintable=False,
    )

    psiquiatricos: Optional[str] = flags(
        default=None,
        sqlite=SQLiteFieldConstraint.NONE,
        tcontrol=InputWidgetType.INPUT_TEXT,
        title="Psiquiátricos",
        showintable=False,
    )

    hospitalizaciones_previas: Optional[str] = flags(
        default=None,
        sqlite=SQLiteFieldConstraint.NONE,
        tcontrol=InputWidgetType.INPUT_TEXT,
        title="Hospitalizaciones Previas",
        showintable=False,
    )
    lb_af: int = flags(
        default=0,
        sqlite=SQLiteFieldConstraint.IGNORE,
        tcontrol=InputWidgetType.SEP,
        title="Antecedentes Familiares",
        required=False,
        showintable=False,
    )

    familiares: Optional[str] = flags(
        default=None,
        title="Informe:",
        sqlite=SQLiteFieldConstraint.NONE,
        tcontrol=InputWidgetType.INPUT_TEXT_RICH,
        showintable=False,
    )

    lb_efps: int = flags(
        default=0,
        sqlite=SQLiteFieldConstraint.IGNORE,
        tcontrol=InputWidgetType.SEP,
        title="Examen Fisico Por Sistemas",
        required=False,
        showintable=False,
    )

    general: Optional[str] = flags(
        default=None,
        sqlite=SQLiteFieldConstraint.NONE,
        tcontrol=InputWidgetType.INPUT_TEXT,
        title="General",
        showintable=False,
    )

    neurologico: Optional[str] = flags(
        default=None,
        sqlite=SQLiteFieldConstraint.NONE,
        tcontrol=InputWidgetType.INPUT_TEXT,
        title="Neurologico",
        showintable=False,
    )

    respiratorio: Optional[str] = flags(
        default=None,
        sqlite=SQLiteFieldConstraint.NONE,
        tcontrol=InputWidgetType.INPUT_TEXT,
        title="Respiratorio",
        showintable=False,
    )

    cardiovascular: Optional[str] = flags(
        default=None,
        sqlite=SQLiteFieldConstraint.NONE,
        tcontrol=InputWidgetType.INPUT_TEXT,
        title="Cardiovascular",
        showintable=False,
    )

    gastrointestinal: Optional[str] = flags(
        default=None,
        sqlite=SQLiteFieldConstraint.NONE,
        tcontrol=InputWidgetType.INPUT_TEXT,
        title="Gastrointestinal",
        showintable=False,
    )

    genitourinario: Optional[str] = flags(
        default=None,
        sqlite=SQLiteFieldConstraint.NONE,
        tcontrol=InputWidgetType.INPUT_TEXT,
        title="Genitourinario",
        showintable=False,
    )

    musculo_esqueletico: Optional[str] = flags(
        default=None,
        sqlite=SQLiteFieldConstraint.NONE,
        tcontrol=InputWidgetType.INPUT_TEXT,
        title="Musculo-esqueletico",
        showintable=False,
    )

    dermatologico: Optional[str] = flags(
        default=None,
        sqlite=SQLiteFieldConstraint.NONE,
        tcontrol=InputWidgetType.INPUT_TEXT,
        title="Dermatologico",
        showintable=False,
    )

    endocrino: Optional[str] = flags(
        default=None,
        sqlite=SQLiteFieldConstraint.NONE,
        tcontrol=InputWidgetType.INPUT_TEXT,
        title="Endocrino",
        showintable=False,
    )

    psiquiatrico: Optional[str] = flags(
        default=None,
        sqlite=SQLiteFieldConstraint.NONE,
        tcontrol=InputWidgetType.INPUT_TEXT,
        title="Psiquiátrico",
        showintable=False,
    )
    lb_ef: int = flags(
        default=0,
        sqlite=SQLiteFieldConstraint.IGNORE,
        tcontrol=InputWidgetType.SEP,
        title="Examen Fisico",
        required=False,
        showintable=False,
    )

    tension: Optional[str] = flags(
        default=None,
        sqlite=SQLiteFieldConstraint.NONE,
        tcontrol=InputWidgetType.INPUT_TEXT,
        title="Tension Arterial",
        showintable=False,
    )

    frecuenciac: Optional[float] = flags(
        default=None,
        sqlite=SQLiteFieldConstraint.NONE,
        tcontrol=InputWidgetType.INPUT_FLOAT,
        title="Frecuencia Cardiaca",
        showintable=False,
    )

    frecuenciar: Optional[float] = flags(
        default=None,
        sqlite=SQLiteFieldConstraint.NONE,
        tcontrol=InputWidgetType.INPUT_FLOAT,
        title="Frecuencia Respiratoria",
        showintable=False,
    )

    temp: Optional[float] = flags(
        default=None,
        sqlite=SQLiteFieldConstraint.NONE,
        tcontrol=InputWidgetType.INPUT_FLOAT,
        title="Temperatura Corporal",
        showintable=False,
    )

    satur: Optional[float] = flags(
        default=None,
        sqlite=SQLiteFieldConstraint.NONE,
        tcontrol=InputWidgetType.INPUT_FLOAT,
        title="Saturacion de Oxigeno",
        showintable=False,
    )

    peso: Optional[float] = flags(
        default=None,
        sqlite=SQLiteFieldConstraint.NONE,
        tcontrol=InputWidgetType.INPUT_FLOAT,
        title="Peso",
        showintable=False,
    )

    talla: Optional[float] = flags(
        default=None,
        sqlite=SQLiteFieldConstraint.NONE,
        tcontrol=InputWidgetType.INPUT_FLOAT,
        title="Talla",
        showintable=False,
    )

    imc: Optional[float] = flags(
        default=None,
        sqlite=SQLiteFieldConstraint.NONE,
        tcontrol=InputWidgetType.INPUT_FLOAT,
        title="IMC",
        showintable=False,
    )
    observaciones: Optional[str] = flags(
        default=None,
        sqlite=SQLiteFieldConstraint.NONE,
        tcontrol=InputWidgetType.INPUT_TEXT_RICH,
        title="Observaciones",
        showintable=False,
    )

    lb_pf: int = flags(
        default=0,
        sqlite=SQLiteFieldConstraint.IGNORE,
        tcontrol=InputWidgetType.SEP,
        title="Profesional",
        required=False,
        showintable=False,
    )
    pfnombre: str = flags(
        default=None,
        sqlite=SQLiteFieldConstraint.NONE,
        tcontrol=InputWidgetType.INPUT_TEXT,
        title="Profesional",
        required=True,
        searchable=True,
        showintable=True,
    )
    pfnumero_registro: str = flags(
        default=None,
        sqlite=SQLiteFieldConstraint.NONE,
        tcontrol=InputWidgetType.INPUT_TEXT,
        title="Numero de Registro",
        required=True,
        showintable=False,
    )
    pfespecialidad: Optional[str] = flags(
        default=None,
        sqlite=SQLiteFieldConstraint.NONE,
        tcontrol=InputWidgetType.INPUT_TEXT,
        title="Especialidad",
        required=True,
        showintable=False,
    )
    pffirma_digital: Optional[str] = flags(
        default=None,
        sqlite=SQLiteFieldConstraint.NONE,
        tcontrol=InputWidgetType.INPUT_TEXT,
        title="Firma",
        required=True,
        showintable=False,
    )
    lb_sg: int = flags(
        default=0,
        sqlite=SQLiteFieldConstraint.IGNORE,
        tcontrol=InputWidgetType.SEP,
        title="Seguimiento",
        required=False,
        showintable=False,
    )

    ls_sg: list[Seguimiento] = flagsv2(
        default_factory=list,
        model=Seguimiento,
        sqlite=SQLiteFieldConstraint.NONE,
        tcontrol=InputWidgetType.LIST,
        title=Empty,
        showintable=False,
    )
    lb_pm: int = flags(
        default=0,
        sqlite=SQLiteFieldConstraint.IGNORE,
        tcontrol=InputWidgetType.SEP,
        title="Plan Manejo",
        required=False,
        showintable=False,
    )
    ls_pm: list[PlanManejo] = flagsv2(
        default_factory=list,
        model=PlanManejo,
        sqlite=SQLiteFieldConstraint.NONE,
        tcontrol=InputWidgetType.LIST,
        title=Empty,
        showintable=False,
    )
