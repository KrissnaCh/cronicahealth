from dataclasses import dataclass, field
from datetime import date
from typing import Optional
import sqlite3
from database.crud import SQLiteFieldConstraint, create_table_sql
from internal import DesignerP, Empty, SQLiteP
from internal.designerflags import DesignerField, InputWidgetType


@dataclass
class MedicalConsultation:
    """
    Modelo que representa una consulta médica general.
    """
    motivo_consulta: str = Empty
    historia_enfermedad_actual: str = Empty
    examen_fisico: str = Empty
    diagnostico: str = Empty
    plan_manejo: str = Empty
    seguimiento_fecha: Optional[date] = None
    seguimiento_observaciones: Optional[str] = None


@dataclass
class InformacionGeneralPaciente:
    """
    Modelo que almacena la información general del paciente.
    """
    id: int = field(default=0, metadata={
        SQLiteP: SQLiteFieldConstraint.PRIMARY_KEY | SQLiteFieldConstraint.UNIQUE,
        DesignerP: DesignerField(InputWidgetType.INPUT_INT, "Codigo", True)
    })

    nombre_completo: Optional[str] = field(default=None, metadata={
        DesignerP: DesignerField(InputWidgetType.INPUT_TEXT, "Nombre Completo")})

    fecha_nacimiento: Optional[date] = field(
        default=None, metadata={DesignerP: DesignerField(InputWidgetType.DATE_PICKER, "Fecha de Nacimiento")})

    edad: Optional[int] = field(default=None, metadata={
                                DesignerP: DesignerField(InputWidgetType.INPUT_INT, "Edad")})

    genero: Optional[str] = field(default=None, metadata={
                                  DesignerP: DesignerField(InputWidgetType.COMBO, "Genero", items=["Masculino", "Femenino"])})

    cedula: Optional[str] = field(default=None, metadata={
        DesignerP: DesignerField(InputWidgetType.INPUT_TEXT, "Cedula")})

    direccion: Optional[str] = field(default=None, metadata={
        DesignerP: DesignerField(InputWidgetType.INPUT_TEXT, "Direccion",required= False)})

    telefono: Optional[str] = field(default=None, metadata={
                                    DesignerP: DesignerField(InputWidgetType.INPUT_TEXT, "Telefono", required=False)})

    email: Optional[str] = field(default=None, metadata={
                                 DesignerP: DesignerField(InputWidgetType.INPUT_TEXT, "Email", required=False)})

    estado_civil: Optional[str] = field(default=None, metadata={
                                        DesignerP: DesignerField(InputWidgetType.COMBO, "Estado Civil",  items=["Soltero", "Casado", "Divorciado", "Viudo", "Otro"])})

    ocupacion: Optional[str] = field(default=None, metadata={
                                     DesignerP: DesignerField(InputWidgetType.INPUT_TEXT, "Ocupacion", required=False)})


@dataclass
class AntecedentesPersonales:
    """
    Modelo que almacena los antecedentes personales del paciente.
    """
    patologicos: Optional[str] = None
    quirurgicos: Optional[str] = None
    alergicos: Optional[str] = None
    traumaticos: Optional[str] = None
    toxicos: Optional[str] = None
    gineco_obstetricos: Optional[str] = None
    psiquiatricos: Optional[str] = None
    hospitalizaciones_previas: Optional[str] = None


@dataclass
class AntecedentesFamiliares:
    """
    Modelo para antecedentes familiares.
    """
    familiares: Optional[str] = None


@dataclass
class ExamenFisicoPorSistemas:
    """
    Modelo de revisión de síntomas por sistemas.
    """
    general: Optional[str] = None
    neurologico: Optional[str] = None
    respiratorio: Optional[str] = None
    cardiovascular: Optional[str] = None
    gastrointestinal: Optional[str] = None
    genitourinario: Optional[str] = None
    musculo_esqueletico: Optional[str] = None
    dermatologico: Optional[str] = None
    endocrino: Optional[str] = None
    psiquiatrico: Optional[str] = None


@dataclass
class ExamenFisico:
    """
    Modelo para el examen físico general.
    """
    signos_vitales: Optional[str] = None
    peso: Optional[float] = None
    talla: Optional[float] = None
    imc: Optional[float] = None
    cabeza_cuello: Optional[str] = None
    torax: Optional[str] = None
    abdomen: Optional[str] = None
    extremidades: Optional[str] = None
    neurologico: Optional[str] = None


@dataclass
class PlanManejo:
    """
    Modelo para el plan de manejo clínico.
    """
    paraclinicos: Optional[str] = None
    medicamentos: Optional[str] = None
    recomendaciones: Optional[str] = None
    remisiones: Optional[str] = None


@dataclass
class Seguimiento:
    """
    Modelo para el seguimiento del paciente.
    """
    fecha_proximo_control: Optional[date] = None
    observaciones_adicionales: Optional[str] = None


@dataclass
class Profesional:
    """
    Modelo que almacena los datos del profesional de la salud.
    """
    nombre: str = Empty
    numero_registro: str = Empty
    especialidad: Optional[str] = None
    firma_digital: Optional[str] = None


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


def make_database(path: str):
    """
    Crea una base de datos SQLite a partir de un conjunto de clases dataclass, 
    generando las tablas correspondientes automáticamente.

    Parámetros:
        path (str): Ruta donde se creará o abrirá el archivo de la base de datos SQLite.

    Funcionamiento:
        - Define una lista de clases dataclass (`instances`) que representan los modelos de datos.
        - Abre una conexión a la base de datos SQLite en la ruta especificada.
        - Para cada clase en la lista:
            - Se genera la sentencia SQL de creación de tabla usando `create_table_sql(instance)`.
            - Se ejecuta la sentencia SQL para crear la tabla si no existe.
            - Si ocurre un error durante la creación de la tabla, imprime el error y la sentencia SQL fallida para ayudar en la depuración.
    """
    instances = [
        MedicalConsultation,
        InformacionGeneralPaciente,
        AntecedentesPersonales,
        AntecedentesFamiliares,
        ExamenFisicoPorSistemas,
        ExamenFisico,
        PlanManejo,
        Seguimiento,
        Profesional,
        HistoriaClinica
    ]
    db: sqlite3.Connection = sqlite3.connect(path)
    for instance in instances:
        try:
            db.execute(create_table_sql(instance))
        except Exception as e:
            print(f"{instance}: {e}")
            print(create_table_sql(instance))
