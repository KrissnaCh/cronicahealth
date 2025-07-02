import copy
from dataclasses import fields, is_dataclass
from datetime import date
from typing import Callable, Optional, Union
import dearpygui.dearpygui as dpg

from database import crud
from internal import CONTROL, ITEMS, READONLY, SEARCHABLE, SHOWINTABLE, TITLE, ActionDesigner, ControlID, InputWidgetType
from internal.ext import align_items
from ui import designer
from ui.designer import SearcherFlag
from ui.designer.builder import DesignerBuilder
from ui.designer.frmtable import FormTableShow
class FormSearcherDesigner:

    def __read_row(self, data):
        self._table_show.add_row(data)

    def __search(self):
        clone = copy.deepcopy(self.model)
        for key, (id, typ) in self.attrs.items():
            if typ == InputWidgetType.DATE_PICKER:
                date_value = dpg.get_value(id[1])
                if date_value:
                    setattr(
                        clone,
                        key,
                        date(
                            year=date_value["year"] + 1900,
                            month=date_value["month"] + 1,
                            day=date_value["month_day"],
                        ),
                    )
            else:
                value = dpg.get_value(id[1])
                if isinstance(value, str):
                    setattr(clone, key, f"%{value}%")
                elif isinstance(value, int) or isinstance(value, float):
                    if value > 0:
                        setattr(clone, key, value)
        query, params = crud.to_select_query(
            clone, ignore_primary_int=True, comparator="Like"
        )
        self._table_show.clear_table()
        crud.execute_select(self.model_type, query, self.__read_row, params)
        dpg.delete_item(self._window_id)
        self._table_show.show()

    def show(self):
        """Muestra la ventana del formulario de detalle."""
        dpg.show_item(self._window_id)

    def __init__(
        self,
        model,
        title: str,
        args: tuple[SearcherFlag, ActionDesigner],
        custom_target: Optional[type] = None,
        custom_show: Optional[Callable] = None,
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
        self._custom_show: Optional[Callable] = custom_show
        self._custom_target = custom_target
        self.model = model
        self._title = title
        self.designer_fields = [
            CONTROL,
            TITLE,
            READONLY,
            ITEMS,
            SEARCHABLE,
            SHOWINTABLE,
        ]

        self.args = args
        self.attrs: dict[str, tuple[ControlID, InputWidgetType]] = {}
        self.model_type = type(model)
        self.builder = DesignerBuilder()
        self._table_show = FormTableShow(
            self._title, self.model, self.args, self._custom_target, self._custom_show
        )

        self.__create_ui()

    def __create_ui(self):
        
        y_pos = designer.window_base_y + designer.window_count * designer.window_spacing
        x_pos = designer.window_base_x + designer.window_count * designer.window_spacing
        """Crea la interfaz de usuario del formulario de detalle."""
        with dpg.mutex():
            with dpg.window(
                label=self._title,
                pos=(x_pos, y_pos),
                autosize=True,
                no_collapse=True,
                show=False,
            ) as self._window_id:
                just = max(
                    (
                        len(f.metadata[TITLE])
                        for f in fields(self.model)
                        if all(key in f.metadata for key in self.designer_fields)
                    ),
                    default=0,
                )

                for f in fields(self.model):
                    if all(key in f.metadata for key in self.designer_fields):
                        if f.metadata[SEARCHABLE] == False:
                            continue
                        match f.metadata[CONTROL]:
                            case InputWidgetType.INPUT_INT:
                                self.attrs[f.name] = (
                                    self.builder.add_input_int(
                                        f.metadata[TITLE].ljust(just),
                                        getattr(self.model, f.name),
                                        False,
                                    ),
                                    InputWidgetType.INPUT_INT,
                                )
                            case InputWidgetType.INPUT_TEXT:
                                self.attrs[f.name] = (
                                    self.builder.add_input_text(
                                        f.metadata[TITLE].ljust(just),
                                        getattr(self.model, f.name),
                                        False,
                                    ),
                                    InputWidgetType.INPUT_TEXT,
                                )
                            case InputWidgetType.INPUT_FLOAT:
                                self.attrs[f.name] = (
                                    self.builder.add_input_float(
                                        f.metadata[TITLE].ljust(just),
                                        getattr(self.model, f.name),
                                        False,
                                    ),
                                    InputWidgetType.INPUT_FLOAT,
                                )
                            case InputWidgetType.DATE_PICKER:
                                self.attrs[f.name] = (
                                    self.builder.add_date_picker_v2(
                                        f.metadata[TITLE].ljust(just),
                                        getattr(self.model, f.name),
                                        False,
                                    ),
                                    InputWidgetType.DATE_PICKER,
                                )
                            case InputWidgetType.COMBO:
                                self.attrs[f.name] = (
                                    self.builder.add_combo(
                                        f.metadata[TITLE].ljust(just),
                                        f.metadata[ITEMS],
                                        getattr(self.model, f.name),
                                        False,
                                    ),
                                    InputWidgetType.COMBO,
                                )
                            case _:
                                pass

                dpg.add_separator()
                with align_items(0, 1):
                    dpg.add_image_button("ico_search", callback=self.__search)

        designer.window_count = (designer.window_count + 1) % 10
        pass