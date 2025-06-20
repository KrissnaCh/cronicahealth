
from datetime import date
import sqlite3
import dearpygui.dearpygui as dpg

from database import crud
from database.models import AntecedentesFamiliares, AntecedentesPersonales, ExamenFisico, ExamenFisicoPorSistemas, HistoriaClinica, InformacionGeneralPaciente, MedicalConsultation, PlanManejo, Profesional, Seguimiento
import internal
from ui import message
from ui.designer import FormDetailDesigner, FormSearcherDesigner, SearcherFlag
from ui.events_application import DbEventAntecedentesFamiliares, DbEventAntecedentesPersonales, DbBasicComand, DbEventExamenFisico, DbEventExamenFisicoPorSistemas


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
