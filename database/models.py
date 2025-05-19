from dataclasses import dataclass, field
from datetime import date
from typing import Optional


from database.crud import SQLiteFieldConstraint
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

    def __init__(
        self,
        motivo_consulta: str,
        historia_enfermedad_actual: str,
        examen_fisico: str,
        diagnostico: str,
        plan_manejo: str,
        seguimiento_fecha: Optional[date] = None,
        seguimiento_observaciones: Optional[str] = None
    ):
        """
        Inicializa una instancia de MedicalConsultation.
        """
        self.motivo_consulta = motivo_consulta
        self.historia_enfermedad_actual = historia_enfermedad_actual
        self.examen_fisico = examen_fisico
        self.diagnostico = diagnostico
        self.plan_manejo = plan_manejo
        self.seguimiento_fecha = seguimiento_fecha
        self.seguimiento_observaciones = seguimiento_observaciones

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
    id:int= field(metadata={SQLiteP: SQLiteFieldConstraint.PRIMARY_KEY|SQLiteFieldConstraint.UNIQUE})
    nombre_completo: str =field(metadata={SQLiteP: SQLiteFieldConstraint.UNIQUE|SQLiteFieldConstraint.AUTOINCREMENT})
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

    def __init__(
        self,
        nombre_completo: str,
        fecha_nacimiento: date,
        edad: Optional[int] = None,
        sexo: str = "",
        genero: Optional[str] = None,
        cedula: str = "",
        direccion: str = "",
        telefono: Optional[str] = None,
        email: Optional[str] = None,
        estado_civil: Optional[str] = None,
        ocupacion: Optional[str] = None
    ):
        """
        Inicializa una instancia de InformacionGeneralPaciente.
        """
        self.nombre_completo = nombre_completo
        self.fecha_nacimiento = fecha_nacimiento
        self.edad = edad
        self.sexo = sexo
        self.genero = genero
        self.cedula = cedula
        self.direccion = direccion
        self.telefono = telefono
        self.email = email
        self.estado_civil = estado_civil
        self.ocupacion = ocupacion

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

    def __init__(
        self,
        patologicos: Optional[str] = None,
        quirurgicos: Optional[str] = None,
        alergicos: Optional[str] = None,
        traumaticos: Optional[str] = None,
        toxicos: Optional[str] = None,
        gineco_obstetricos: Optional[str] = None,
        psiquiatricos: Optional[str] = None,
        hospitalizaciones_previas: Optional[str] = None
    ):
        """
        Inicializa una instancia de AntecedentesPersonales.
        """
        self.patologicos = patologicos
        self.quirurgicos = quirurgicos
        self.alergicos = alergicos
        self.traumaticos = traumaticos
        self.toxicos = toxicos
        self.gineco_obstetricos = gineco_obstetricos
        self.psiquiatricos = psiquiatricos
        self.hospitalizaciones_previas = hospitalizaciones_previas

@dataclass
class AntecedentesFamiliares:
    """
    Modelo para antecedentes familiares.

    Atributos:
        familiares (Optional[str]): Enfermedades hereditarias o frecuentes en la familia.
    """
    familiares: Optional[str] = None

    def __init__(self, familiares: Optional[str] = None):
        """
        Inicializa una instancia de AntecedentesFamiliares.
        """
        self.familiares = familiares

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

    def __init__(
        self,
        general: Optional[str] = None,
        neurologico: Optional[str] = None,
        respiratorio: Optional[str] = None,
        cardiovascular: Optional[str] = None,
        gastrointestinal: Optional[str] = None,
        genitourinario: Optional[str] = None,
        musculo_esqueletico: Optional[str] = None,
        dermatologico: Optional[str] = None,
        endocrino: Optional[str] = None,
        psiquiatrico: Optional[str] = None
    ):
        """
        Inicializa una instancia de ExamenFisicoPorSistemas.
        """
        self.general = general
        self.neurologico = neurologico
        self.respiratorio = respiratorio
        self.cardiovascular = cardiovascular
        self.gastrointestinal = gastrointestinal
        self.genitourinario = genitourinario
        self.musculo_esqueletico = musculo_esqueletico
        self.dermatologico = dermatologico
        self.endocrino = endocrino
        self.psiquiatrico = psiquiatrico

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

    def __init__(
        self,
        signos_vitales: Optional[str] = None,
        peso: Optional[float] = None,
        talla: Optional[float] = None,
        imc: Optional[float] = None,
        cabeza_cuello: Optional[str] = None,
        torax: Optional[str] = None,
        abdomen: Optional[str] = None,
        extremidades: Optional[str] = None,
        neurologico: Optional[str] = None
    ):
        """
        Inicializa una instancia de ExamenFisico.
        """
        self.signos_vitales = signos_vitales
        self.peso = peso
        self.talla = talla
        self.imc = imc
        self.cabeza_cuello = cabeza_cuello
        self.torax = torax
        self.abdomen = abdomen
        self.extremidades = extremidades
        self.neurologico = neurologico

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

    def __init__(
        self,
        paraclinicos: Optional[str] = None,
        medicamentos: Optional[str] = None,
        recomendaciones: Optional[str] = None,
        remisiones: Optional[str] = None
    ):
        """
        Inicializa una instancia de PlanManejo.
        """
        self.paraclinicos = paraclinicos
        self.medicamentos = medicamentos
        self.recomendaciones = recomendaciones
        self.remisiones = remisiones

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

    def __init__(
        self,
        fecha_proximo_control: Optional[date] = None,
        observaciones_adicionales: Optional[str] = None
    ):
        """
        Inicializa una instancia de Seguimiento.
        """
        self.fecha_proximo_control = fecha_proximo_control
        self.observaciones_adicionales = observaciones_adicionales

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

    def __init__(
        self,
        nombre: str,
        numero_registro: str,
        especialidad: Optional[str] = None,
        firma_digital: Optional[str] = None
    ):
        """
        Inicializa una instancia de Profesional.
        """
        self.nombre = nombre
        self.numero_registro = numero_registro
        self.especialidad = especialidad
        self.firma_digital = firma_digital

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

    def __init__(
        self,
        paciente: InformacionGeneralPaciente,
        motivo_consulta: str,
        enfermedad_actual: str,
        antecedentes_personales: AntecedentesPersonales,
        antecedentes_familiares: AntecedentesFamiliares,
        examen_sistemas: ExamenFisicoPorSistemas,
        examen_fisico: ExamenFisico,
        impresion_diagnostica: str,
        plan_manejo: PlanManejo,
        seguimiento: Seguimiento,
        profesional: Profesional
    ):
        """
        Inicializa una instancia de HistoriaClinica.
        """
        self.paciente = paciente
        self.motivo_consulta = motivo_consulta
        self.enfermedad_actual = enfermedad_actual
        self.antecedentes_personales = antecedentes_personales
        self.antecedentes_familiares = antecedentes_familiares
        self.examen_sistemas = examen_sistemas
        self.examen_fisico = examen_fisico
        self.impresion_diagnostica = impresion_diagnostica
        self.plan_manejo = plan_manejo
        self.seguimiento = seguimiento
        self.profesional = profesional