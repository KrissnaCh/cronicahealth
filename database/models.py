from dataclasses import dataclass, field
from datetime import date
from typing import Optional
import sqlite3
from database.crud import SQLiteFieldConstraint, create_table_sql
from internal import SQLiteP


@dataclass
class MedicalConsultation:
    """
    Modelo que representa una consulta médica general.

    Atributos:
        motivo_consulta (str): Motivo de consulta (texto libre).
        historia_enfermedad_actual (str): Historia de enfermedad actual (texto libre, largo).
        examen_fisico (str): Examen físico, signos vitales y exploración por sistemas (texto libre, largo).
        diagnostico (str): Diagnóstico principal.
        plan_manejo (str): Plan de manejo propuesto.
        seguimiento_fecha (Optional[date]): Fecha del próximo control (opcional).
        seguimiento_observaciones (Optional[str]): Observaciones adicionales del seguimiento (opcional).
    """
    motivo_consulta: str
    historia_enfermedad_actual: str
    examen_fisico: str
    diagnostico: str
    plan_manejo: str
    seguimiento_fecha: Optional[date] = None
    seguimiento_observaciones: Optional[str] = None


@dataclass
class InformacionGeneralPaciente:
    """
    Modelo que almacena la información general del paciente.

    Atributos:
        nombre_completo (str): Nombre completo del paciente.
        fecha_nacimiento (date): Fecha de nacimiento.
        edad (Optional[int]): Edad del paciente (opcional).
        sexo (str): Sexo biológico (masculino/femenino/otro).
        genero (Optional[str]): Género (opcional).
        cedula (str): Número de cédula o documento de identidad.
        direccion (str): Dirección de residencia.
        telefono (Optional[str]): Teléfono de contacto (opcional).
        email (Optional[str]): Correo electrónico (opcional).
        estado_civil (Optional[str]): Estado civil (opcional).
        ocupacion (Optional[str]): Ocupación (opcional).
    """
    id: int = field(metadata={
                    SQLiteP: SQLiteFieldConstraint.PRIMARY_KEY | SQLiteFieldConstraint.UNIQUE})
    nombre_completo: str
    fecha_nacimiento: date
    edad: Optional[int] = None
    sexo: str = ""
    genero: Optional[str] = None
    cedula: str = ""
    direccion: str = ""
    telefono: Optional[str] = None
    email: Optional[str] = None
    estado_civil: Optional[str] = None
    ocupacion: Optional[str] = None


@dataclass
class AntecedentesPersonales:
    """
    Modelo que almacena los antecedentes personales del paciente.

    Atributos:
        patologicos (Optional[str]): Enfermedades previas.
        quirurgicos (Optional[str]): Antecedentes quirúrgicos.
        alergicos (Optional[str]): Alergias conocidas.
        traumaticos (Optional[str]): Antecedentes de trauma.
        toxicos (Optional[str]): Consumo de alcohol, tabaco, drogas.
        gineco_obstetricos (Optional[str]): Información gineco-obstétrica (solo mujeres).
        psiquiatricos (Optional[str]): Antecedentes psiquiátricos.
        hospitalizaciones_previas (Optional[str]): Otras hospitalizaciones.
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

    Atributos:
        familiares (Optional[str]): Enfermedades hereditarias o frecuentes en la familia.
    """
    familiares: Optional[str] = None


@dataclass
class ExamenFisicoPorSistemas:
    """
    Modelo de revisión de síntomas por sistemas.

    Atributos:
        general, neurologico, respiratorio, cardiovascular, gastrointestinal,
        genitourinario, musculo_esqueletico, dermatologico, endocrino, psiquiatrico:
        (Optional[str]) Revisión por sistema.
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

    Atributos:
        signos_vitales (Optional[str]): Signos vitales (TA, FC, FR, Temp, Saturación).
        peso (Optional[float]): Peso en kg.
        talla (Optional[float]): Talla en metros.
        imc (Optional[float]): Índice de masa corporal.
        cabeza_cuello (Optional[str]): Examen de cabeza y cuello.
        torax (Optional[str]): Examen de tórax.
        abdomen (Optional[str]): Examen abdominal.
        extremidades (Optional[str]): Examen de extremidades.
        neurologico (Optional[str]): Examen neurológico.
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

    Atributos:
        paraclinicos (Optional[str]): Paraclínicos solicitados.
        medicamentos (Optional[str]): Medicamentos formulados.
        recomendaciones (Optional[str]): Recomendaciones al paciente.
        remisiones (Optional[str]): Remisiones a otros servicios.
    """
    paraclinicos: Optional[str] = None
    medicamentos: Optional[str] = None
    recomendaciones: Optional[str] = None
    remisiones: Optional[str] = None


@dataclass
class Seguimiento:
    """
    Modelo para el seguimiento del paciente.

    Atributos:
        fecha_proximo_control (Optional[date]): Fecha del próximo control.
        observaciones_adicionales (Optional[str]): Observaciones adicionales.
    """
    fecha_proximo_control: Optional[date] = None
    observaciones_adicionales: Optional[str] = None


@dataclass
class Profesional:
    """
    Modelo que almacena los datos del profesional de la salud.

    Atributos:
        nombre (str): Nombre del profesional.
        numero_registro (str): Número de registro o tarjeta profesional.
        especialidad (Optional[str]): Especialidad médica (opcional).
        firma_digital (Optional[str]): Firma digital (puede ser ruta de archivo o base64, opcional).
    """
    nombre: str
    numero_registro: str
    especialidad: Optional[str] = None
    firma_digital: Optional[str] = None


@dataclass
class HistoriaClinica:
    """
    Modelo integral que agrupa toda la historia clínica de un paciente.

    Atributos:
        paciente (InformacionGeneralPaciente): Información general del paciente.
        motivo_consulta (str): Motivo de consulta.
        enfermedad_actual (str): Descripción de la enfermedad actual.
        antecedentes_personales (AntecedentesPersonales): Antecedentes personales del paciente.
        antecedentes_familiares (AntecedentesFamiliares): Antecedentes familiares.
        examen_sistemas (ExamenFisicoPorSistemas): Examen físico por sistemas.
        examen_fisico (ExamenFisico): Examen físico general.
        impresion_diagnostica (str): Impresión diagnóstica principal.
        plan_manejo (PlanManejo): Plan de manejo.
        seguimiento (Seguimiento): Seguimiento del paciente.
        profesional (Profesional): Datos del profesional responsable.
    """
    paciente: InformacionGeneralPaciente
    motivo_consulta: str
    enfermedad_actual: str
    antecedentes_personales: AntecedentesPersonales
    antecedentes_familiares: AntecedentesFamiliares
    examen_sistemas: ExamenFisicoPorSistemas
    examen_fisico: ExamenFisico
    impresion_diagnostica: str
    plan_manejo: PlanManejo
    seguimiento: Seguimiento
    profesional: Profesional


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
