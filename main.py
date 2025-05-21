#import database
from datetime import date
import dearpygui.dearpygui as dpg

import database.crud
import database.models


if __name__ == "__main__":
    print(database.crud.create_table_sql(database.models.InformacionGeneralPaciente))

    consulta = database.models.MedicalConsultation(
        motivo_consulta="Dolor de cabeza persistente",
        historia_enfermedad_actual="Paciente refiere dolor de cabeza desde hace 3 días, sin fiebre.",
        examen_fisico="PA: 120/80 mmHg, FC: 75 lpm, conciencia lúcida, sin hallazgos neurológicos.",
        diagnostico="Cefalea tensional",
        plan_manejo="Reposo, hidratación y paracetamol 500mg cada 8h por 3 días.",
        seguimiento_fecha=date(2025, 6, 1),
        seguimiento_observaciones="Revisar si hay nuevos síntomas, especialmente fiebre o visión borrosa."
    )
    print(database.crud.to_insert_sql(consulta))
    pass