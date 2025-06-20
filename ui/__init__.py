
from datetime import date
import sqlite3
import dearpygui.dearpygui as dpg

from database import crud
from database.models import AntecedentesFamiliares, AntecedentesPersonales, ExamenFisico, ExamenFisicoPorSistemas, HistoriaClinica, InformacionGeneralPaciente, MedicalConsultation, PlanManejo, Profesional, Seguimiento
import internal
from ui import message
from ui.designer import FormDetailDesigner, FormSearcherDesigner, SearcherFlag
from ui.events_application import DbEventAntecedentesFamiliares, DbEventAntecedentesPersonales, DbBasicComand, DbEventExamenFisico, DbEventExamenFisicoPorSistemas, DbEventProfesional,DbSeguimiento,DbEventPlanManejo


class Application:

    def __callback_patient_insert(self, sender):
        dlg = FormDetailDesigner(
            InformacionGeneralPaciente(),
            "Insertar Paciente",
            save_callback=DbBasicComand.ui_insert,
        )
        dlg.show()

    def __callback_patient_update(self, sender):
        dlg = FormSearcherDesigner(
            InformacionGeneralPaciente(),
            "Actualizar Paciente",
            (SearcherFlag.UPDATE, DbBasicComand.ui_update)
        )
        dlg.show()

    def __callback_patient_delete(self, sender):
        dlg = FormSearcherDesigner(
            InformacionGeneralPaciente(),
            "Eliminar Paciente",
            (SearcherFlag.DELETE, DbBasicComand.ui_delete)
        )
        dlg.show()

    def __callback_patient_consult(self, sender):
        dlg = FormSearcherDesigner(
            InformacionGeneralPaciente(),
            "Consultar Paciente",
            (SearcherFlag.CONSULT, None)
        )
        dlg.show()

    def __callback_show_info(self, sender):
        message.show(
            title="Informacion",
            message="Esta aplicacion es un sistema de gestion de citas medicas.",
            buttons=message.MessageBoxButtons.OK,
            on_close=None
        )
        

    def __callback_personal_background_insert(self, sender):
        dlg = FormSearcherDesigner(
            InformacionGeneralPaciente(),
            "Insertar Antecedentes Personales",
            (SearcherFlag.INSERT, DbEventAntecedentesPersonales.ui_insert),
            custom_target= AntecedentesPersonales
        )
        dlg.show()
    def __callback_personal_background_delete(self, sender):
        dlg = FormSearcherDesigner(
            InformacionGeneralPaciente(),
            "Eliminar Antecedentes Personales",
            (SearcherFlag.DELETE, DbBasicComand.ui_delete),
            custom_target= AntecedentesPersonales,
            custom_show=DbEventAntecedentesPersonales.ui_custom_show
        )
        dlg.show()
        
    def __callback_personal_background_update(self, sender):
        dlg = FormSearcherDesigner(
            InformacionGeneralPaciente(),
            "Actualizar Antecedentes Personales",
            (SearcherFlag.UPDATE, DbBasicComand.ui_update),
            custom_target= AntecedentesPersonales,
            custom_show=DbEventAntecedentesPersonales.ui_custom_show
        )
        dlg.show()
        
    def __callback_personal_background_consutl(self, sender):
        dlg = FormSearcherDesigner(
            InformacionGeneralPaciente(),
            "Consultar Antecedentes Personales",
            (SearcherFlag.CONSULT, None),
            custom_target= AntecedentesPersonales,
            custom_show=DbEventAntecedentesPersonales.ui_custom_show
        )
        dlg.show()

    def __callback_familiar_background_insert(self, sender):
        dlg = FormSearcherDesigner(
            InformacionGeneralPaciente(),
            "Insertar Antecedentes Familiares",
            (SearcherFlag.INSERT, DbEventAntecedentesFamiliares.ui_insert),
            custom_target=AntecedentesFamiliares
        )
        dlg.show()

    def __callback_familiar_background_delete(self, sender):
        dlg = FormSearcherDesigner(
            InformacionGeneralPaciente(),
            "Eliminar Antecedentes Familiares",
            (SearcherFlag.DELETE, DbBasicComand.ui_delete),
            custom_target=AntecedentesFamiliares,
            custom_show=DbEventAntecedentesFamiliares.ui_custom_show
            
        )
        dlg.show()

    def __callback_familiar_background_update(self, sender):
        dlg = FormSearcherDesigner(
            InformacionGeneralPaciente(),
            "Modificar Antecedentes Familiares",
            (SearcherFlag.UPDATE, DbBasicComand.ui_update),
            custom_target=AntecedentesFamiliares,
            custom_show=DbEventAntecedentesFamiliares.ui_custom_show
        )
        dlg.show()

    def __callback_familiar_background_consutl(self, sender):
        dlg = FormSearcherDesigner(
            InformacionGeneralPaciente(),
            "Consultar Antecedentes Familiares",
            (SearcherFlag.CONSULT, None),
            custom_target=AntecedentesFamiliares,
            custom_show=DbEventAntecedentesFamiliares.ui_custom_show
        )
        dlg.show()

    def __callback_physical_examination_by_systems_insert(self, sender):
        dlg = FormSearcherDesigner(
            InformacionGeneralPaciente(),
            "Insertar Examen Fisico por Sistemas",
            (SearcherFlag.INSERT, DbEventExamenFisicoPorSistemas.ui_insert),
            custom_target=ExamenFisicoPorSistemas
        )
        dlg.show()

    def __callback_physical_examination_by_systems_delete(self, sender):
        dlg = FormSearcherDesigner(
            InformacionGeneralPaciente(),
            "Eliminar Examen Fisico por Sistemas",
            (SearcherFlag.DELETE, DbBasicComand.ui_delete),
            custom_target=ExamenFisicoPorSistemas,
            custom_show=DbEventExamenFisicoPorSistemas.ui_custom_show
        )
        dlg.show()

    def __callback_physical_examination_by_systems_update(self, sender):
        dlg = FormSearcherDesigner(
            InformacionGeneralPaciente(),
            "Modificar Examen Fisico por Sistemas",
            (SearcherFlag.UPDATE, DbBasicComand.ui_update),
            custom_target=ExamenFisicoPorSistemas,
            custom_show=DbEventExamenFisicoPorSistemas.ui_custom_show
        )
        dlg.show()

    def __callback_physical_examination_by_systems_consutl(self, sender):
        dlg = FormSearcherDesigner(
            InformacionGeneralPaciente(),
            "Consultar Examen Fisico por Sistemas",
            (SearcherFlag.CONSULT, None),
            custom_target=ExamenFisicoPorSistemas,
            custom_show=DbEventExamenFisicoPorSistemas.ui_custom_show
        )
        dlg.show()

    def __callback_physical_examination_insert(self, sender):
        dlg = FormSearcherDesigner(
            InformacionGeneralPaciente(),
            "Insertar Examen Fisico",
            (SearcherFlag.INSERT, DbEventExamenFisico.ui_insert),
            custom_target=ExamenFisico
        )
        dlg.show()

    def __callback_physical_examination_delete(self, sender):
        dlg = FormSearcherDesigner(
            InformacionGeneralPaciente(),
            "Eliminar Examen Fisico",
            (SearcherFlag.DELETE, DbBasicComand.ui_delete),
            custom_target=ExamenFisico,
            custom_show=DbEventExamenFisico.ui_custom_show
        )
        dlg.show()

    def __callback_physical_examination_update(self, sender):
        dlg = FormSearcherDesigner(
            InformacionGeneralPaciente(),
            "Modificar Examen Fisico",
            (SearcherFlag.UPDATE, DbBasicComand.ui_update),
            custom_target=ExamenFisico,
            custom_show=DbEventExamenFisico.ui_custom_show
        )
        dlg.show()

    def __callback_physical_examination_consutl(self, sender):
        dlg = FormSearcherDesigner(
            InformacionGeneralPaciente(),
            "Consultar Examen Fisico",
            (SearcherFlag.CONSULT, None),
            custom_target=ExamenFisico,
            custom_show=DbEventExamenFisico.ui_custom_show
        )
        dlg.show()

    def __callback_management_insert(self, sender):
        dlg = FormSearcherDesigner(
            InformacionGeneralPaciente(),
            "Insertar Plan de Manejo",
            (SearcherFlag.INSERT, DbEventPlanManejo.ui_insert),
            custom_target=PlanManejo
        )
        dlg.show()

    def __callback_management_delete(self, sender):
        dlg = FormSearcherDesigner(
            InformacionGeneralPaciente(),
            "Eliminar Plan de Manejo",
            (SearcherFlag.DELETE, DbBasicComand.ui_delete),
            custom_target=PlanManejo,
            custom_show=DbEventPlanManejo.ui_custom_show
        )
        dlg.show()

    def __callback_management_update(self, sender):
        dlg = FormSearcherDesigner(
            InformacionGeneralPaciente(),
            "Modificar Plan de Manejo",
            (SearcherFlag.UPDATE, DbBasicComand.ui_update),
            custom_target=PlanManejo,
            custom_show=DbEventPlanManejo.ui_custom_show
        )
        dlg.show()

    def __callback_management_consutl(self, sender):
        dlg = FormSearcherDesigner(
            InformacionGeneralPaciente(),
            "Consultar Plan de Manejo",
            (SearcherFlag.CONSULT, None),
            custom_target=PlanManejo,
            custom_show=DbEventPlanManejo.ui_custom_show
        )
        dlg.show()

    def __callback_tracing_insert(self, sender):
        dlg = FormSearcherDesigner(
            InformacionGeneralPaciente(),
            "Insertar Seguimiento",
            (SearcherFlag.INSERT, DbSeguimiento.ui_insert),
            custom_target=Seguimiento
        )
        dlg.show()

    def __callback_tracing_delete(self, sender):
        dlg = FormSearcherDesigner(
            InformacionGeneralPaciente(),
            "Eliminar Seguimiento",
            (SearcherFlag.DELETE, DbBasicComand.ui_delete),
            custom_target=Seguimiento,
            custom_show=DbSeguimiento.ui_custom_show
        )
        dlg.show()

    def __callback_tracing_update(self, sender):
        dlg = FormSearcherDesigner(
            InformacionGeneralPaciente(),
            "Modificar Seguimiento",
            (SearcherFlag.UPDATE, DbBasicComand.ui_update),
            custom_target=Seguimiento,
            custom_show=DbSeguimiento.ui_custom_show
        )
        dlg.show()

    def __callback_tracing_consutl(self, sender):
        dlg = FormSearcherDesigner(
            InformacionGeneralPaciente(),
            "Consultar Seguimiento",
            (SearcherFlag.CONSULT, None),
            custom_target=Seguimiento,
            custom_show=DbSeguimiento.ui_custom_show
        )
        dlg.show()

    def __callback_professional_insert(self, sender):
        dlg = FormSearcherDesigner(
            InformacionGeneralPaciente(),
            "Insertar Seguimiento",
            (SearcherFlag.INSERT, DbSeguimiento.ui_insert),
            custom_target=Profesional
        )
        dlg.show()

    def __callback_professional_delete(self, sender):
        dlg = FormSearcherDesigner(
            Profesional(),
            "Eliminar Profesional",
            (SearcherFlag.DELETE, DbBasicComand.ui_delete),
            custom_target=Profesional,
            custom_show=DbEventProfesional.ui_custom_show
        )
        dlg.show()

    def __callback_professional_update(self, sender):
        dlg = FormSearcherDesigner(
            Profesional(),
            "Modificar Profesional",
            (SearcherFlag.UPDATE, DbBasicComand.ui_update),
            custom_target=Profesional,
            custom_show=DbEventProfesional.ui_custom_show
        )
        dlg.show()

    def __callback_professional_consutl(self, sender):
        dlg = FormSearcherDesigner(
            Profesional(),
            "Consultar Profesional",
            (SearcherFlag.CONSULT, None),
            custom_target=Profesional,
            custom_show=DbEventProfesional.ui_custom_show
        )
        dlg.show()

    def __init__(self, cli_args: list[str]):
        dpg.create_context()

        with dpg.font_registry():
            default_font = dpg.add_font("assents/ChivoMono.ttf", 20*2)
            dpg.bind_font(default_font)

        dpg.create_viewport(title='Main Window', width=600, height=400)

        with dpg.viewport_menu_bar():
            with dpg.menu(label="Paciente"):
                dpg.add_menu_item(label="Insertar",
                                  callback=self.__callback_patient_insert)
                dpg.add_menu_item(label="Eliminar",
                                  callback=self.__callback_patient_delete)
                dpg.add_menu_item(label="Modificar",
                                  callback=self.__callback_patient_update)
                dpg.add_menu_item(label="Consultar",
                                  callback=self.__callback_patient_consult)
                with dpg.menu(label="Antecedentes Personales"):
                    dpg.add_menu_item(label="Insertar",
                                      callback=self.__callback_personal_background_insert)
                    dpg.add_menu_item(label="Eliminar",
                                      callback=self.__callback_personal_background_delete)
                    dpg.add_menu_item(label="Modificar",
                                      callback=self.__callback_personal_background_update)
                    dpg.add_menu_item(label="Consultar",
                                      callback=self.__callback_personal_background_consutl)
                    
                with dpg.menu(label="Antecedentes Familiares"):
                    dpg.add_menu_item(label="Insertar",
                                      callback=self.__callback_familiar_background_insert)
                    dpg.add_menu_item(label="Eliminar",
                                      callback=self.__callback_familiar_background_delete)
                    dpg.add_menu_item(label="Modificar",
                                      callback=self.__callback_familiar_background_update)
                    dpg.add_menu_item(label="Consultar",
                                      callback=self.__callback_familiar_background_consutl)
                    
                with dpg.menu(label="Examen fisico por Sistemas"):
                    dpg.add_menu_item(label="Insertar",
                                      callback=self.__callback_physical_examination_by_systems_insert)
                    dpg.add_menu_item(label="Eliminar",
                                      callback=self.__callback_physical_examination_by_systems_delete)
                    dpg.add_menu_item(label="Modificar",
                                      callback=self.__callback_physical_examination_by_systems_update)
                    dpg.add_menu_item(label="Consultar",
                                      callback=self.__callback_physical_examination_by_systems_consutl)
                
                with dpg.menu(label="Examen fisico"):
                    dpg.add_menu_item(label="Insertar",
                                      callback=self.__callback_physical_examination_insert)
                    dpg.add_menu_item(label="Eliminar",
                                      callback=self.__callback_physical_examination_delete)
                    dpg.add_menu_item(label="Modificar",
                                      callback=self.__callback_physical_examination_update)
                    dpg.add_menu_item(label="Consultar",
                                      callback=self.__callback_physical_examination_consutl)

            with dpg.menu(label="Gestion Adaptativa"):
                with dpg.menu(label="Planes de Manejo"):
                    dpg.add_menu_item(label="Insertar",
                                      callback=self.__callback_management_insert)
                    dpg.add_menu_item(label="Eliminar",
                                      callback=self.__callback_management_delete)
                    dpg.add_menu_item(label="Modificar",
                                      callback=self.__callback_management_update)
                    dpg.add_menu_item(label="Consultar",
                                      callback=self.__callback_management_consutl)
                with dpg.menu(label="Seguimiento"):
                    dpg.add_menu_item(label="Insertar",
                                      callback=self.__callback_tracing_insert)
                    dpg.add_menu_item(label="Eliminar",
                                      callback=self.__callback_tracing_delete)
                    dpg.add_menu_item(label="Modificar",
                                      callback=self.__callback_tracing_update)
                    dpg.add_menu_item(label="Consultar",
                                      callback=self.__callback_tracing_consutl)
                with dpg.menu(label="Profecional"):
                    dpg.add_menu_item(label="Insertar",
                                      callback=self.__callback_professional_insert)
                    dpg.add_menu_item(label="Eliminar",
                                      callback=self.__callback_professional_delete)
                    dpg.add_menu_item(label="Modificar",
                                      callback=self.__callback_professional_update)
                    dpg.add_menu_item(label="Consultar",
                                      callback=self.__callback_professional_consutl)
                                  

            dpg.add_menu_item(label="Informacion",
                              callback=self.__callback_show_info)

    def run(self):
        crud.make_database([
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
        ])
        dpg.configure_app(docking=True, docking_space=True)
        dpg.set_global_font_scale(0.5)
        dpg.setup_dearpygui()
        dpg.show_viewport(maximized=True)
        dpg.start_dearpygui()
        dpg.destroy_context()
