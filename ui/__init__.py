
from datetime import date
import dearpygui.dearpygui as dpg

from database.models import InformacionGeneralPaciente
from ui.designer import FormDetailDesigner, FormSearcherDesigner


class Application:

    def print_me(self, sender):
        print(f"Menu Item: {sender}")

    def __callback_patient_insert(self, sender):
        dlg = FormSearcherDesigner(InformacionGeneralPaciente(id=1,
                                                              nombre_completo="Juan Pérez García",
                                                              fecha_nacimiento=date(
                                                                  2025, 1, 1),
                                                              edad=39,
                                                              genero="hombre",
                                                              cedula="12345678",
                                                              direccion="Calle Falsa 123, Ciudad",
                                                              telefono="555-1234",
                                                              email="juan.perez@email.com",
                                                              estado_civil="soltero",
                                                              ocupacion="Ingeniero"))

        pass

    def __callback_patient_update(self, sender):
        pass

    def __callback_patient_delete(self, sender):
        pass

    def __callback_show_info(self, sender):
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
        dpg.set_global_font_scale(0.5)
        dpg.setup_dearpygui()
        dpg.show_viewport(maximized=True)
        dpg.start_dearpygui()
        dpg.destroy_context()
