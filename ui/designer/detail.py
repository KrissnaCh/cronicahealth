import copy
from dataclasses import fields, is_dataclass
from datetime import date
from typing import Callable, Optional, Union
import dearpygui.dearpygui as dpg
from internal.ext import align_items
from ui import designer
from ui.designer.builder import DesignerBuilder
import ui.message as msgbox
from internal import (
    CONTROL,
    ITEMS,
    LISTMODEL,
    READONLY,
    REQUIRED,
    SEARCHABLE,
    TITLE,
    ActionDesigner,
    ControlID,
    Empty,
    InputWidgetType,
    is_empty_or_whitespace,
)
from ui.message import MessageBoxButtons


class FormDetailDesigner:

    # en revision
    def __model_callback(self, sender):
        user_data = dpg.get_item_user_data(sender)
        if user_data:
            frm = FormDetailDesigner(
                user_data[1],
                f"Editar {user_data[0]}",
                # save_callback=self.__btn_callback,
                # update_callback=self.__btn_callback,
                # delete_callback=self.__btn_callback,
                closeonexec=True,
            )
            frm.show()
        else:
            raise ValueError("No se proporcionó un modelo.")

    def __btn_callback(self, sender):
        """Maneja el evento de clic en los botones del formulario."""
        user_data = dpg.get_item_user_data(sender)
        try:
            self.missing_fields = Empty
            for key in self.attrs_required:
                value = dpg.get_value(self.attrs[key][0][0])

                # incluir validador para tipo de datos mejor
                if value and is_empty_or_whitespace(
                    str(dpg.get_value(self.attrs[key][0][1]))
                ):
                    self.missing_fields += f" - {value.replace('*', '').strip()}\n"
            if self.missing_fields:
                raise ValueError(
                    f"Los siguientes campos requeridos están vacíos o ausentes: \n\n{self.missing_fields}\n"
                )

            if user_data:
                old_model = copy.deepcopy(self.model)
                # Actualiza el modelo con los valores de los controles
                for key, (id, typ) in self.attrs.items():
                    if typ == InputWidgetType.DATE_PICKER:
                        date_value = dpg.get_value(id[1])
                        if date_value:
                            if isinstance(date_value, str):
                                # Parsear fecha desde string en formato dd/mm/yyyy
                                try:
                                    day, month, year = map(int, date_value.split("/"))
                                    setattr(self.model, key, date(year, month, day))
                                except Exception:
                                    setattr(self.model, key, None)
                            else:
                                setattr(
                                    self.model,
                                    key,
                                    date(
                                        year=date_value["year"] + 1900,
                                        month=date_value["month"] + 1,
                                        day=date_value["month_day"],
                                    ),
                                )
                    elif typ == InputWidgetType.INPUT_JSON:
                        """bandera de entrada de lista"""
                        setattr(self.model, key,self.builder.get_list(id[1]))
                    else:
                        setattr(self.model, key, dpg.get_value(id[1]))
                if self._orig:
                    user_data(self._orig, old_model, self.model)
                else:
                    user_data(old_model, self.model)

            if self._closeonexec:
                dpg.delete_item(self._window_id)
        except ValueError as e:
            msgbox.show("Error", str(e), MessageBoxButtons.OK, on_close=None)
            pass

    def show(self, onclose:Optional[Callable] = None):
        """Muestra la ventana del formulario de detalle."""
        if onclose:
            self.__close = onclose
        dpg.show_item(self._window_id)

    def _onclose(self, sender):
        if self.__close:
            self.__close()
        pass

    def __init__(
        self,
        model,
        title: str,
        save_callback: ActionDesigner = None,
        update_callback: ActionDesigner = None,
        delete_callback: ActionDesigner = None,
        closeonexec=True,
        is_readonly=False,
        orig=None,
    ):
        """Inicializa el diseñador de formularios de detalle.
        Args:
            model: Una instancia de dataclass que define el modelo del formulario.
            title: Título de la ventana del formulario.
        Raises:
            ValueError: Si el modelo no es una instancia de dataclass.
        """
        # Verifica si el modelo es una instancia de dataclass
        if not is_dataclass(model):
            raise ValueError("entrada debe ser una instancia de dataclass.")

        self._window_id: Union[int, str] = 0
        self.model = model
        self.__close:Optional[Callable]  = None
        self._title = title
        self.designer_fields = [CONTROL, TITLE, READONLY, REQUIRED, ITEMS, SEARCHABLE]

        # callbacks para guardar, actualizar y eliminar
        self._save_callback = save_callback
        self._update_callback = update_callback
        self._delete_callback = delete_callback

        # Indica si se debe cerrar la ventana al ejecutar una acción.
        self._closeonexec = closeonexec
        self.__is_readonly = is_readonly
        self.model_type = type(model)
        self.builder = DesignerBuilder()
        self._orig = orig

        self.attrs: dict[str, tuple[ControlID, InputWidgetType]] = {}
        self.attrs_required: list[str] = []
        self.missing_fields = Empty
        self.__create_ui()

    def mark_required(self, value, required) -> str:
        """Marca un campo como requerido en el formulario.
        Args:
            value: El texto del campo.
            required: Un booleano que indica si el campo es requerido.
        Returns:
            str: El texto del campo, con un asterisco (*) al final si es requerido.
        """
        val = value if isinstance(value, str) else Empty.join(value)
        return f"{val} *" if required else val

    def __create_ui(self):

        y_pos = designer.window_base_y + designer.window_count * designer.window_spacing
        x_pos = designer.window_base_x + designer.window_count * designer.window_spacing
        """Crea la interfaz de usuario del formulario de detalle."""
        # Genera un ID único para la ventana
        from itertools import batched

        viewport_width = dpg.get_viewport_client_width()
        viewport_height = dpg.get_viewport_client_height()
        with dpg.window(
            label=self._title,
            autosize=True,
            max_size=(viewport_width - 300, viewport_height - 300),
            pos=(x_pos, y_pos),
            no_collapse=True,
            show=False,
            on_close=self._onclose
        ) as self._window_id:
            # Calcula la longitud máxima de las etiquetas para la alineación, usando una expresión generadora para eficiencia
            just = max(
                (
                    len(self.mark_required(f.metadata[TITLE], f.metadata[REQUIRED]))
                    for f in fields(self.model)
                    if all(key in f.metadata for key in self.designer_fields)
                ),
                default=0,
            )
            __fields = [
                f
                for f in fields(self.model)
                if all(key in f.metadata for key in self.designer_fields)
            ]
            
            __fields = [
                f for f in __fields if f.metadata[CONTROL] != InputWidgetType.NONE
            ]
            
            dt = {}
            last = None
            for f in __fields:
                if f.metadata[CONTROL] == InputWidgetType.SEP:
                    dt[f.metadata[TITLE]] = []
                    last = f.metadata[TITLE]
                else:
                    if last:
                        dt[last].append(f)

            for key in dt:
                self.builder.add_separator(key)

                for chunk in batched(dt[key], 2):
                    with dpg.group(horizontal=True):
                        for f in chunk:
                            self.makecontrol(just, f)
                            pass
            if not dt:
                for chunk in batched(__fields, 2):
                    with dpg.group(horizontal=True):
                        for f in chunk:
                            self.makecontrol(just, f)

            count_callbacks = sum(
                cb is not None
                for cb in [
                    self._save_callback,
                    self._update_callback,
                    self._delete_callback,
                ]
            )
            if count_callbacks > 0:
                dpg.add_separator()

                with align_items(0, count_callbacks):  # Alinea los botones a la derecha
                    if self._save_callback:
                        dpg.add_image_button(
                            texture_tag="ico_save",
                            callback=self.__btn_callback,
                            user_data=self._save_callback,
                        )
                    if self._update_callback:
                        dpg.add_image_button(
                            texture_tag="ico_update",
                            callback=self.__btn_callback,
                            user_data=self._update_callback,
                        )
                    if self._delete_callback:
                        dpg.add_image_button(
                            texture_tag="ico_delete",
                            callback=self.__btn_callback,
                            user_data=self._delete_callback,
                        )
        designer.window_count = (designer.window_count + 1) % 10
        pass

    def makecontrol(self, just, f):
        readonly = True if self.__is_readonly else f.metadata[READONLY]
        match f.metadata[CONTROL]:
            case InputWidgetType.INPUT_INT:
                self.attrs[f.name] = (
                    self.builder.add_input_int(
                        self.mark_required(
                            f.metadata[TITLE], f.metadata[REQUIRED]
                        ).ljust(just),
                        getattr(self.model, f.name),
                        readonly,
                    ),
                    InputWidgetType.INPUT_INT,
                )
            case InputWidgetType.INPUT_TEXT:
                self.attrs[f.name] = (
                    self.builder.add_input_text(
                        self.mark_required(
                            f.metadata[TITLE], f.metadata[REQUIRED]
                        ).ljust(just),
                        getattr(self.model, f.name),
                        readonly,
                    ),
                    InputWidgetType.INPUT_TEXT,
                )
            case InputWidgetType.INPUT_TEXT_RICH:
                self.attrs[f.name] = (
                    self.builder.add_input_text_v2(
                        self.mark_required(
                            f.metadata[TITLE], f.metadata[REQUIRED]
                        ).ljust(just),
                        getattr(self.model, f.name),
                        readonly,
                    ),
                    InputWidgetType.INPUT_TEXT,
                )
            case InputWidgetType.INPUT_FLOAT:
                self.attrs[f.name] = (
                    self.builder.add_input_float(
                        self.mark_required(
                            f.metadata[TITLE], f.metadata[REQUIRED]
                        ).ljust(just),
                        getattr(self.model, f.name),
                        readonly,
                    ),
                    InputWidgetType.INPUT_FLOAT,
                )
            case InputWidgetType.LIST:
                if not f.metadata.get(LISTMODEL):
                    raise ValueError(
                        f"El campo {f.name} debe tener un modelo de lista definido en {LISTMODEL}."
                    )
                self.attrs[f.name] = (
                    self.builder.add_input_list(
                        f.metadata[LISTMODEL],
                        getattr(self.model, f.name),
                        readonly,
                        self.designer_fields,
                    ),
                    InputWidgetType.INPUT_JSON,
                )
            case InputWidgetType.DATE_PICKER:
                self.attrs[f.name] = (
                    self.builder.add_date_picker(
                        self.mark_required(
                            f.metadata[TITLE], f.metadata[REQUIRED]
                        ).ljust(just),
                        getattr(self.model, f.name),
                        readonly,
                    ),
                    InputWidgetType.DATE_PICKER,
                )
            case InputWidgetType.COMBO:
                self.attrs[f.name] = (
                    self.builder.add_combo(
                        self.mark_required(
                            f.metadata[TITLE], f.metadata[REQUIRED]
                        ).ljust(just),
                        f.metadata[ITEMS],
                        getattr(self.model, f.name),
                        readonly,
                    ),
                    InputWidgetType.COMBO,
                )
            case InputWidgetType.SEP:
                self.builder.add_separator(f.metadata[TITLE])
            case InputWidgetType.MODEL:
                self.attrs[f.name] = (
                    self.builder.add_input_model(
                        self.mark_required(
                            f.metadata[TITLE], f.metadata[REQUIRED]
                        ).ljust(just),
                        self.__model_callback,
                        (f.name, getattr(self.model, f.name)),
                        readonly,
                    ),
                    InputWidgetType.MODEL,
                )
            case _:
                pass
        if f.metadata[REQUIRED] == True:
            self.attrs_required.append(f.name)
