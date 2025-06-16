from dataclasses import dataclass, field
from datetime import date
from typing import Optional
import sqlite3
from database.crud import SQLiteFieldConstraint, create_table_sql
from internal import Empty, InputWidgetType, flags


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
                    sqlite=SQLiteFieldConstraint.PRIMARY_KEY | SQLiteFieldConstraint.UNIQUE,
                    tcontrol=InputWidgetType.NONE,
                    title="Codigo",
                    readonly=True, showintable=False)

    nombre_completo: Optional[str] = flags(default=None,
                                           sqlite=SQLiteFieldConstraint.NONE,
                                           tcontrol=InputWidgetType.INPUT_TEXT,
                                           required=True,
                                           title="Nombre Completo")

    fecha_nacimiento: Optional[date] = flags(default=None,
                                             sqlite=SQLiteFieldConstraint.NONE,
                                             required=True,
                                             tcontrol=InputWidgetType.DATE_PICKER,
                                             title="Fecha de Nacimiento", showintable=False)

    edad: Optional[int] = flags(default=None,
                                sqlite=SQLiteFieldConstraint.NONE,
                                required=True,
                                tcontrol=InputWidgetType.INPUT_INT,
                                title="Edad")

    genero: Optional[str] = flags(default=None,
                                  sqlite=SQLiteFieldConstraint.NONE,
                                  tcontrol=InputWidgetType.COMBO,
                                  required=True,
                                  title="Genero",
                                  items=["Masculino", "Femenino"])

    cedula: Optional[str] = flags(default=None,
                                  sqlite=SQLiteFieldConstraint.NONE,
                                  required=True,
                                  tcontrol=InputWidgetType.INPUT_TEXT,
                                  title="Cedula")

    direccion: Optional[str] = flags(default=None, sqlite=SQLiteFieldConstraint.NONE,
                                     tcontrol=InputWidgetType.INPUT_TEXT,
                                     title="Direccion",
                                     required=False,showintable= False)

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
                                            "Otro"],showintable=False)

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
    familiares: Optional[str] = None


@dataclass
class ExamenFisicoPorSistemas:
    """
    Modelo de revisión de síntomas por sistemas.
    """
    general: Optional[str] = flags(default=None,
                                   sqlite=SQLiteFieldConstraint.NONE,
                                   tcontrol=InputWidgetType.INPUT_TEXT,
                                   title="")

    neurologico: Optional[str] = flags(default=None,
                                       sqlite=SQLiteFieldConstraint.NONE,
                                       tcontrol=InputWidgetType.INPUT_TEXT,
                                       title="")

    respiratorio: Optional[str] = flags(default=None,
                                        sqlite=SQLiteFieldConstraint.NONE,
                                        tcontrol=InputWidgetType.INPUT_TEXT,
                                        title="")

    cardiovascular: Optional[str] = flags(default=None,
                                          sqlite=SQLiteFieldConstraint.NONE,
                                          tcontrol=InputWidgetType.INPUT_TEXT,
                                          title="")

    gastrointestinal: Optional[str] = flags(default=None,
                                            sqlite=SQLiteFieldConstraint.NONE,
                                            tcontrol=InputWidgetType.INPUT_TEXT,
                                            title="")

    genitourinario: Optional[str] = flags(default=None,
                                          sqlite=SQLiteFieldConstraint.NONE,
                                          tcontrol=InputWidgetType.INPUT_TEXT,
                                          title="")

    musculo_esqueletico: Optional[str] = flags(default=None,
                                               sqlite=SQLiteFieldConstraint.NONE,
                                               tcontrol=InputWidgetType.INPUT_TEXT,
                                               title="")

    dermatologico: Optional[str] = flags(default=None,
                                         sqlite=SQLiteFieldConstraint.NONE,
                                         tcontrol=InputWidgetType.INPUT_TEXT,
                                         title="")

    endocrino: Optional[str] = flags(default=None,
                                     sqlite=SQLiteFieldConstraint.NONE,
                                     tcontrol=InputWidgetType.INPUT_TEXT,
                                     title="")

    psiquiatrico: Optional[str] = flags(default=None,
                                        sqlite=SQLiteFieldConstraint.NONE,
                                        tcontrol=InputWidgetType.INPUT_TEXT,
                                        title="")


@dataclass
class ExamenFisico:
    """
    Modelo para el examen físico general.
    """
    signos_vitales: Optional[str] = flags(default=None,
                                          sqlite=SQLiteFieldConstraint.NONE,
                                          tcontrol=InputWidgetType.INPUT_TEXT,
                                          title="")

    peso: Optional[float] = flags(default=None,
                                  sqlite=SQLiteFieldConstraint.NONE,
                                  tcontrol=InputWidgetType.INPUT_FLOAT,
                                  title="")

    talla: Optional[float] = flags(default=None,
                                   sqlite=SQLiteFieldConstraint.NONE,
                                   tcontrol=InputWidgetType.INPUT_FLOAT,
                                   title="")

    imc: Optional[float] = flags(default=None,
                                 sqlite=SQLiteFieldConstraint.NONE,
                                 tcontrol=InputWidgetType.INPUT_FLOAT,
                                 title="")

    cabeza_cuello: Optional[str] = flags(default=None,
                                         sqlite=SQLiteFieldConstraint.NONE,
                                         tcontrol=InputWidgetType.INPUT_TEXT,
                                         title="")

    torax: Optional[str] = flags(default=None,
                                 sqlite=SQLiteFieldConstraint.NONE,
                                 tcontrol=InputWidgetType.INPUT_TEXT,
                                 title="")

    abdomen: Optional[str] = flags(default=None,
                                   sqlite=SQLiteFieldConstraint.NONE,
                                   tcontrol=InputWidgetType.INPUT_TEXT,
                                   title="")

    extremidades: Optional[str] = flags(default=None,
                                        sqlite=SQLiteFieldConstraint.NONE,
                                        tcontrol=InputWidgetType.INPUT_TEXT,
                                        title="")

    neurologico: Optional[str] = flags(default=None,
                                       sqlite=SQLiteFieldConstraint.NONE,
                                       tcontrol=InputWidgetType.INPUT_TEXT,
                                       title="")


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
