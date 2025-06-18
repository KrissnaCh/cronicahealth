
from datetime import date
import dearpygui.dearpygui as dpg

from database.models import InformacionGeneralPaciente
from ui import message
from ui.designer import FormDetailDesigner, FormSearcherDesigner, SearcherFlag


class Application:
    def __patient_save(self, old, new):

        print(f"Old: {old}")
        print(f"New: {new}")

        pass

    def __callback_patient_insert(self, sender):
        dlg = FormDetailDesigner(
            InformacionGeneralPaciente(),
            "Insertar Paciente",
            save_callback=self.__patient_save,
        )
        dlg.show()


    def __callback_patient_update(self, sender):
        dlg = FormSearcherDesigner(
            InformacionGeneralPaciente(),
            "Actualizar Paciente",
            flag=SearcherFlag.UPDATE
        )
        dlg.show()
        pass

    def __callback_patient_delete(self, sender):
        dlg = FormSearcherDesigner(
            InformacionGeneralPaciente(),
            "Actualizar Paciente",
            flag=SearcherFlag.DELETE
        )
        dlg.show()
        pass

    def __callback_show_info(self, sender):
        message.show(
            title="Informacion",
            message="Esta aplicacion es un sistema de gestion de citas medicas.",
            buttons=message.MessageBoxButtons.OK,
            on_close=lambda result: print(f"Dialog closed with result: {result}")
        )
        pass

    def __callback_MedicalConsultation_new(self, sender):
        pass

    def __callback_MedicalConsultation_history(self, sender):
        pass

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

            with dpg.menu(label="Consulta Medica"):
                dpg.add_menu_item(
                    label="Nueva", callback=self.__callback_MedicalConsultation_new)
                dpg.add_menu_item(
                    label="Historial", callback=self.__callback_MedicalConsultation_history)

            with dpg.menu(label="Citas"):
                dpg.add_menu_item(
                    label="Pendientes", callback=self.__callback_MedicalConsultation_new)
                dpg.add_menu_item(
                    label="Completadas", callback=self.__callback_MedicalConsultation_history)
                dpg.add_menu_item(
                    label="Reporte General", callback=self.__callback_MedicalConsultation_history)

            dpg.add_menu_item(label="Informacion",
                              callback=self.__callback_show_info)

    def run(self):
        dpg.configure_app(docking=True, docking_space=True)
        dpg.set_global_font_scale(0.5)
        dpg.setup_dearpygui()
        dpg.show_viewport(maximized=True)
        dpg.start_dearpygui()
        dpg.destroy_context()
