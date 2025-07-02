import dearpygui.dearpygui as dpg
import os
from database import crud
from database.models import (
    InformacionGeneralPaciente,
    MedicalConsultation,
    PlanManejo,
    Seguimiento,
)
from ui import message
from ui.designer import  SearcherFlag, regtexture
from ui.designer.detail import FormDetailDesigner
from ui.designer.searcher import FormSearcherDesigner
from ui.events_application import (
    DbBasicComand,
    
)


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
            (SearcherFlag.UPDATE, DbBasicComand.ui_update),
        )
        dlg.show()

    def __callback_patient_delete(self, sender):
        dlg = FormSearcherDesigner(
            InformacionGeneralPaciente(),
            "Eliminar Paciente",
            (SearcherFlag.DELETE, DbBasicComand.ui_delete),
        )
        dlg.show()

    def __callback_patient_consult(self, sender):
        dlg = FormSearcherDesigner(
            InformacionGeneralPaciente(),
            "Consultar Paciente",
            (SearcherFlag.CONSULT, None),
        )
        dlg.show()


    def __init__(self, cli_args: list[str]):
        dpg.create_context()

        with dpg.font_registry():
            default_font = dpg.add_font("assents/ChivoMono.ttf", 20 * 2)
            dpg.bind_font(default_font)

        dpg.create_viewport(title="Main Window", width=600, height=400)

        with dpg.viewport_menu_bar():
            with dpg.menu(label="Paciente"):
                dpg.add_menu_item(
                    label="Insertar", callback=self.__callback_patient_insert
                )
                dpg.add_menu_item(
                    label="Eliminar", callback=self.__callback_patient_delete
                )
                dpg.add_menu_item(
                    label="Modificar", callback=self.__callback_patient_update
                )
                dpg.add_menu_item(
                    label="Consultar", callback=self.__callback_patient_consult
                )



    def run(self):
        # Cargar imagen de fondo y dibujarla centrada y escalada al viewport
        regtexture("assents/ico_delete.png","ico_delete")
        regtexture("assents/ico_save.png","ico_save")
        regtexture("assents/ico_update.png","ico_update")
        regtexture("assents/ico_search.png","ico_search")
        regtexture("assents/ico_add.png","ico_add")
        regtexture("assents/ico_info.png","ico_info")

        bg_path = os.path.join("assents", "background.png")
        self._bg_draw_image_id = None
        self._bg_drawlist_id = None
        self._bg_texture_id = None
        self._bg_img_size = None
        if os.path.exists(bg_path):
            width, height, channels, data = dpg.load_image(bg_path)
            self._bg_img_size = (width, height)
            with dpg.texture_registry():
                self._bg_texture_id = dpg.add_static_texture(width, height, data)
            with dpg.window(
                no_title_bar=True,
                no_move=True,
                no_resize=True,
                no_collapse=True,
                no_close=True,
                no_bring_to_front_on_focus=True,
                pos=(0, 0),
                tag="__bg_window",
            ) as win_id:
                self._bg_drawlist_id = dpg.add_drawlist(width=width, height=height)
                self._bg_draw_image_id = dpg.draw_image(
                    self._bg_texture_id,
                    (0, 0),
                    (width, height),
                    parent=self._bg_drawlist_id,
                )
            dpg.set_primary_window(win_id, True)

            def update_bg_image(sender, app_data):
                if not (
                    self._bg_img_size
                    and self._bg_drawlist_id
                    and self._bg_draw_image_id
                ):
                    return
                vp_width, vp_height = (
                    dpg.get_viewport_width(),
                    dpg.get_viewport_height(),
                )
                img_w, img_h = self._bg_img_size
                # Centrar la imagen sin escalar
                x0 = (vp_width - img_w) // 2
                y0 = (vp_height - img_h) // 2
                x1 = x0 + img_w
                y1 = y0 + img_h
                dpg.configure_item(
                    self._bg_drawlist_id, width=vp_width, height=vp_height - 40
                )
                dpg.configure_item(self._bg_draw_image_id, pmin=[x0, y0], pmax=[x1, y1])

            dpg.set_viewport_resize_callback(update_bg_image)
            # Llamar una vez al inicio
            update_bg_image(None, None)

        # dpg.configure_app(docking=True, docking_space=True)
        crud.make_database(
            [
                MedicalConsultation,
                InformacionGeneralPaciente,
            ]
        )
        with dpg.theme() as global_theme:
            with dpg.theme_component(dpg.mvAll):

                dpg.add_theme_style(
                    dpg.mvStyleVar_FrameRounding, 8, category=dpg.mvThemeCat_Core
                )
                dpg.add_theme_style(
                    dpg.mvStyleVar_FramePadding, 10, 10, category=dpg.mvThemeCat_Core
                )
                dpg.add_theme_color(
                    dpg.mvThemeCol_Border,
                    (0, 255, 39, 89),
                    category=dpg.mvThemeCat_Core,
                )
                dpg.add_theme_color(
                    dpg.mvThemeCol_BorderShadow,
                    (0, 0, 0, 0),
                    category=dpg.mvThemeCat_Core,
                )
                dpg.add_theme_color(
                    dpg.mvThemeCol_FrameBg,
                    (51, 55, 51, 255),
                    category=dpg.mvThemeCat_Core,
                )
                dpg.add_theme_color(
                    dpg.mvThemeCol_FrameBgHovered,
                    (29, 236, 39, 103),
                    category=dpg.mvThemeCat_Core,
                )
                dpg.add_theme_color(
                    dpg.mvThemeCol_FrameBgActive,
                    (0, 200, 39, 153),
                    category=dpg.mvThemeCat_Core,
                )
                dpg.add_theme_color(
                    dpg.mvThemeCol_TitleBgActive,
                    (15, 135, 39, 255),
                    category=dpg.mvThemeCat_Core,
                )

                dpg.add_theme_color(
                    dpg.mvThemeCol_ScrollbarBg,
                    (51, 51, 39, 255),
                    category=dpg.mvThemeCat_Core,
                )
                dpg.add_theme_color(
                    dpg.mvThemeCol_ScrollbarGrab,
                    (82, 82, 39, 255),
                    category=dpg.mvThemeCat_Core,
                )
                dpg.add_theme_color(
                    dpg.mvThemeCol_ScrollbarGrabHovered,
                    (90, 90, 39, 255),
                    category=dpg.mvThemeCat_Core,
                )
                dpg.add_theme_color(
                    dpg.mvThemeCol_ScrollbarGrabActive,
                    (90, 90, 39, 255),
                    category=dpg.mvThemeCat_Core,
                )

                dpg.add_theme_color(
                    dpg.mvThemeCol_CheckMark,
                    (0, 119, 39, 153),
                    category=dpg.mvThemeCat_Core,
                )
                dpg.add_theme_color(
                    dpg.mvThemeCol_SliderGrab,
                    (29, 151, 39, 103),
                    category=dpg.mvThemeCat_Core,
                )
                dpg.add_theme_color(
                    dpg.mvThemeCol_SliderGrabActive,
                    (0, 119, 39, 153),
                    category=dpg.mvThemeCat_Core,
                )
                dpg.add_theme_color(
                    dpg.mvThemeCol_Button,
                    (51, 51, 39, 255),
                    category=dpg.mvThemeCat_Core,
                )
                dpg.add_theme_color(
                    dpg.mvThemeCol_ButtonHovered,
                    (29, 151, 39, 103),
                    category=dpg.mvThemeCat_Core,
                )
                dpg.add_theme_color(
                    dpg.mvThemeCol_ButtonActive,
                    (0, 119, 39, 153),
                    category=dpg.mvThemeCat_Core,
                )

                dpg.add_theme_color(
                    dpg.mvThemeCol_Header,
                    (51, 51, 39, 255),
                    category=dpg.mvThemeCat_Core,
                )
                dpg.add_theme_color(
                    dpg.mvThemeCol_HeaderHovered,
                    (29, 151, 39, 103),
                    category=dpg.mvThemeCat_Core,
                )
                dpg.add_theme_color(
                    dpg.mvThemeCol_HeaderActive,
                    (0, 119, 39, 153),
                    category=dpg.mvThemeCat_Core,
                )

        # dpg.show_tool(dpg.mvTool_Style)
        dpg.bind_theme(global_theme)
        dpg.set_global_font_scale(0.5)
        dpg.setup_dearpygui()
        dpg.show_viewport(maximized=True)

        dpg.start_dearpygui()
        dpg.destroy_context()