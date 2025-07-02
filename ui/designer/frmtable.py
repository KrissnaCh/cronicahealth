from dataclasses import fields
from typing import Any, Callable, Optional
import dearpygui.dearpygui as dpg

from internal import (
    CONTROL,
    ITEMS,
    READONLY,
    SEARCHABLE,
    SHOWINTABLE,
    TITLE,
    ActionDesigner,
)
from ui import designer
from ui.designer import SearcherFlag
from ui.designer.detail import FormDetailDesigner


class FormTableBase:
    def __init__(
        self,
        title,
        model,
        args: tuple[SearcherFlag, ActionDesigner],
        custom_target: Optional[type] = None,
        custom_show: Optional[Callable] = None,
    ) -> None:
        self._title = title
        self._model = model
        self._custom_target = custom_target
        self._custom_show = custom_show
        self._args = args
        self._designer_fields = [
            CONTROL,
            TITLE,
            READONLY,
            ITEMS,
            SEARCHABLE,
            SHOWINTABLE,
        ]

        self._current_model: Optional[object] = None
        self._num_columns = sum(
            1
            for f in fields(self._model)
            if all(key in f.metadata for key in self._designer_fields)
            and f.metadata[SHOWINTABLE]
        )
        self._on_selected: Callable = lambda: None
        self._ids_table: dict[int | str, list] = {}

    def add_row(self, data: Any):
        columns = [
            f
            for f in fields(self._model)
            if all(key in f.metadata for key in self._designer_fields)
            and f.metadata[SHOWINTABLE]
        ]

        with dpg.table_row(parent=self._table_id) as rowid:
            self._ids_table[rowid] = []
            for f in columns:
                selectable = dpg.add_selectable(
                    label=getattr(data, f.name),
                    span_columns=True,
                    callback=self.__row_clicked,
                )
                dpg.set_item_user_data(selectable, (rowid, data))
                self._ids_table[rowid].append(selectable)
        pass

    def clear_table(self):
        self._ids_table.clear()
        children_to_delete = dpg.get_item_children(
            self._table_id, 1
        )  # 1 para la ranura "children"
        if children_to_delete:
            for child in children_to_delete:
                dpg.delete_item(child)

    def __row_clicked(self, sender, value, user_data):
        """Maneja el evento de selección de una fila en la tabla."""
        if value:
            rowid, data = user_data
            for rid, selectables in self._ids_table.items():
                if rid != rowid:
                    for selectable in selectables:
                        dpg.set_value(selectable, False)
            self._current_model = data

    def __show_selection(self, sender):
        self._on_selected()
        if self._current_model:
            if self._custom_show:
                self._custom_show(self._current_model, self._title, self._args)
            else:
                match self._args[0]:
                    case SearcherFlag.UPDATE:
                        FormDetailDesigner(
                            self._current_model,
                            title=self._title,
                            update_callback=self._args[1],
                        ).show()
                    case SearcherFlag.CONSULT:
                        FormDetailDesigner(
                            self._current_model, title=self._title, is_readonly=True
                        ).show()
                    case SearcherFlag.DELETE:
                        FormDetailDesigner(
                            self._current_model,
                            title=self._title,
                            delete_callback=self._args[1],
                            is_readonly=True,
                        ).show()
                    case SearcherFlag.INSERT:
                        if self._custom_target:
                            FormDetailDesigner(
                                self._custom_target(),
                                title=self._title,
                                save_callback=self._args[1],
                                is_readonly=False,
                                orig=self._current_model,
                            ).show()

    def build(self):
        dpg.add_image_button("ico_info", callback=self.__show_selection)
        with dpg.table(
            height=300,
            row_background=True,
            policy=dpg.mvTable_SizingFixedFit,
            borders_innerH=True,
            borders_outerH=True,
            borders_innerV=True,
            borders_outerV=True,
            clipper=True,
        ) as self._table_id:
            columns = [
                f
                for f in fields(self._model)
                if all(key in f.metadata for key in self._designer_fields)
                and f.metadata[SHOWINTABLE]
            ]
            for f in columns:
                dpg.add_table_column(label=f.metadata[TITLE])


class FormTableShow(FormTableBase):

    def show(self):
        dpg.show_item(self._window_id)

    def close(self):
        dpg.delete_item(self._window_id)

    def __init__(
        self,
        title,
        model,
        args: tuple[SearcherFlag, ActionDesigner],
        custom_target: Optional[type] = None,
        custom_show: Optional[Callable] = None,
    ) -> None:
        super().__init__(title, model, args, custom_target, custom_show)
        self._on_selected = self.close
        self._window_id: Union[int, str] = None  # type: ignore
        self.__create_ui()

    def __create_ui(self):
        y_pos = designer.window_base_y + designer.window_count * designer.window_spacing
        x_pos = designer.window_base_x + designer.window_count * designer.window_spacing
        with dpg.window(
            label="Tabla de " + self._title,
            pos=(x_pos, y_pos),
            no_collapse=True,
            show=False,
        ) as self._window_id:
            self.build()
            designer.window_count = (designer.window_count + 1) % 10
        pass
