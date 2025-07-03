from dataclasses import Field, fields
from datetime import date
from typing import Any, Optional, Union
import dearpygui.dearpygui as dpg

from internal import SHOWINTABLE, TITLE, ControlID


class DesignerBuilder:
    """Clase para construir controles de formulario de manera sencilla."""

    def __init__(self):
        self._ids_table_v2: dict[int | str, dict[int | str, list]] = {}
        self._cols: dict[int | str, list[Field[Any]]] = {}
        self._models: dict[int | str, Any] = {}
        self._current_model: dict[int | str, Any] = {}
        """Posibles controles con multiples tablas"""
        pass

    def add_input_model(self, label, callback, userdata, _readonly) -> ControlID:
        with dpg.group(horizontal=True):
            id = dpg.add_text(label)
            return (
                id,
                dpg.add_button(
                    default_value="Consultar" if _readonly else "Editar",
                    readonly=_readonly,
                    callback=callback,
                    user_data=userdata,
                ),
            )

    def add_input_text(self, label, default_value, _readonly) -> ControlID:
        """Agrega un campo de entrada de texto al formulario.
        Args:
            label: El texto de la etiqueta del campo.
            default_value: El valor predeterminado del campo.
            _readonly: Un booleano que indica si el campo es de solo lectura.
        Returns:
            ControlID: Una tupla que contiene el ID del texto de la etiqueta y el ID del campo de entrada.
        """
        with dpg.group(horizontal=True):
            id = dpg.add_text(label)
            return (
                id,
                dpg.add_input_text(
                    default_value=default_value if default_value else "",
                    readonly=_readonly,
                ),
            )

    def add_input_text_v2(self, label, default_value, _readonly) -> ControlID:
        """Agrega un campo de entrada de texto al formulario.
        Args:
            label: El texto de la etiqueta del campo.
            default_value: El valor predeterminado del campo.
            _readonly: Un booleano que indica si el campo es de solo lectura.
        Returns:
            ControlID: Una tupla que contiene el ID del texto de la etiqueta y el ID del campo de entrada.
        """
        with dpg.group(horizontal=True):
            id = dpg.add_text(label)
            return (
                id,
                dpg.add_input_text(
                    default_value=default_value if default_value else "",
                    readonly=_readonly,
                    multiline=True,
                    height=400,
                ),
            )

    def add_input_int(self, label, default_value, _readonly) -> ControlID:
        """Agrega un campo de entrada de número entero al formulario.
        Args:
            label: El texto de la etiqueta del campo.
            default_value: El valor predeterminado del campo.
            _readonly: Un booleano que indica si el campo es de solo lectura.
        Returns:
            ControlID: Una tupla que contiene el ID del texto de la etiqueta y el ID del campo de entrada.
        """
        if _readonly == False:
            with dpg.group(horizontal=True):
                id = dpg.add_text(label)
                return (
                    id,
                    dpg.add_input_int(
                        default_value=default_value if default_value else 0,
                        min_value=0,
                        min_clamped=True,
                    ),
                )
        else:
            return self.add_input_text(label, str(default_value), _readonly)

    def add_separator(self, label: str):
        dpg.add_separator()
        dpg.add_text(label.upper(), indent=15)
        dpg.add_separator()

    def add_input_float(self, label, default_value, _readonly) -> ControlID:
        """Agrega un campo de entrada de número flotante al formulario.
        Args:
            label: El texto de la etiqueta del campo.
            default_value: El valor predeterminado del campo.
            _readonly: Un booleano que indica si el campo es de solo lectura.
        Returns:
            ControlID: Una tupla que contiene el ID del texto de la etiqueta y el ID del campo de entrada.
        """
        if _readonly == False:
            with dpg.group(horizontal=True):
                id = dpg.add_text(label)
                return (
                    id,
                    dpg.add_input_float(
                        default_value=default_value if default_value else 0,
                        min_value=0,
                        min_clamped=True,
                        readonly=_readonly,
                    ),
                )

        else:
            return self.add_input_text(label, str(default_value), _readonly)

    def __row_clicked(self, sender, value, user_data):
        """Maneja el evento de selección de una fila en la tabla."""
        if value:
            rowid, tbid = user_data
            for rid, selectables in self._ids_table_v2[tbid].items():
                if rid != rowid:
                    for selectable in selectables:
                        dpg.set_value(selectable, False)
            self._current_model[tbid] = rowid

    def get_list(self, id: Union[str, int])->Optional[list]:
        if id in self._ids_table_v2:
            return [dpg.get_item_user_data(val) for val in self._ids_table_v2[id].keys() if val]
        else:
            return None
        

    def add_input_list(
        self, model, default_value: list, _readonly, designer_fields
    ) -> ControlID:
        with dpg.group():
            with dpg.table(
                height=300,
                row_background=True,
                policy=dpg.mvTable_SizingFixedFit,
                borders_innerH=True,
                borders_outerH=True,
                borders_innerV=True,
                borders_outerV=True,
                clipper=True,
            ) as tbid:
                self._ids_table_v2[tbid] = {}
                self._models[tbid] = model
                self._cols[tbid] = [
                    f
                    for f in fields(self._models[tbid])
                    if all(key in f.metadata for key in designer_fields)
                    and f.metadata[SHOWINTABLE]
                ]

                for f in self._cols[tbid]:
                    dpg.add_table_column(label=f.metadata[TITLE])
                for data in default_value:
                    self.__add_row(tbid, data)
            with dpg.group(horizontal=True):

                dpg.add_image_button(
                    texture_tag="ico_add",
                    callback=self.__btn_callback,
                    user_data=(tbid, 0),
                )

                dpg.add_image_button(
                    texture_tag="ico_update",
                    callback=self.__btn_callback,
                    user_data=(tbid, 1),
                )
                dpg.add_image_button(
                    texture_tag="ico_delete",
                    callback=self.__btn_callback,
                    user_data=(tbid, 2),
                )
        return (
            -1,
            tbid,
        )

    def __btn_callback(self, sender):
        
        dpg.disable_item(sender)

        from ui.designer.detail import (
            FormDetailDesigner,
        )  # Import local para evitar import circular

        value = dpg.get_item_user_data(sender)
        if value:
            tbid, action = value
            def add_handler(old, new):
                nonlocal tbid
                self.__add_row(tbid, new)
                dpg.enable_item(sender)

            def update_handler(old, new):
                nonlocal tbid
                delete()
                self.__add_row(tbid,new)
                dpg.enable_item(sender)
            def close_handler():
                dpg.enable_item(sender)

            def delete():
                if tbid in self._current_model:
                    rowid = self._current_model[tbid]
                    if rowid in self._ids_table_v2[tbid]:
                        del self._ids_table_v2[tbid][rowid]
                    dpg.delete_item(rowid)
                    del self._current_model[tbid]
                    dpg.enable_item(sender)

            match action:
                case 0:
                    """Agregar una nueva fila a la tabla."""
                    dlg = FormDetailDesigner(
                        self._models[tbid](),
                        "Nuevo",
                        save_callback=add_handler,
                    )
                    dlg.show(close_handler)
                case 1:
                    """Actualizar la fila seleccionada en la tabla."""
                    if tbid in self._current_model:
                        rowid = self._current_model[tbid]
                        data =dpg.get_item_user_data(rowid)
                        dlg = FormDetailDesigner(
                            data,
                            "Actualizar",
                            save_callback=update_handler,
                        )
                        dlg.show(close_handler)
                    pass
                case 2:
                    # Eliminar la fila seleccionada de la tabla.
                    delete()
                    pass
        pass

    def __add_row(self, tbid, data):
        with dpg.table_row(parent=tbid) as rowid:
            self._ids_table_v2[tbid][rowid] = []
            for f in self._cols[tbid]:
                attr = getattr(data, f.name)
                if isinstance(attr, date):
                    label_value = attr.strftime("%d/%m/%Y")
                else:
                    label_value = attr
                selectable = dpg.add_selectable(
                    label=label_value,
                    span_columns=True,
                    callback=self.__row_clicked,
                )
                dpg.set_item_user_data(selectable, (rowid, tbid))
                self._ids_table_v2[tbid][rowid].append(selectable)
            dpg.set_item_user_data(rowid, data)

    def add_combo(self, label, items, default_value, readonly) -> ControlID:
        """Agrega un campo de selección desplegable al formulario.
        Args:
            label: El texto de la etiqueta del campo.
            items: Una lista de elementos para el campo desplegable.
            default_value: El valor predeterminado del campo.
            readonly: Un booleano que indica si el campo es de solo lectura.
        Returns:
            ControlID: Una tupla que contiene el ID del texto de la etiqueta y el ID del campo desplegable.
        """
        if readonly == False:
            with dpg.group(horizontal=True):
                id = dpg.add_text(label)
                return (
                    id,
                    dpg.add_combo(
                        items=items,
                        default_value=default_value if default_value else "",
                    ),
                )
        else:
            return self.add_input_text(label, default_value, readonly)

    def add_date_picker(self, label, default_date: date, readonly) -> ControlID:
        """Agrega un selector de fecha al formulario.
        Args:
            label: El texto de la etiqueta del campo.
            default_date: La fecha predeterminada para el selector de fecha.
            readonly: Un booleano que indica si el campo es de solo lectura.
        Returns:
            ControlID: Una tupla que contiene el ID del texto de la etiqueta y el ID del selector de fecha.
        """
        if readonly == False:
            with dpg.group(horizontal=True):
                id = dpg.add_text(label)
                if default_date:
                    return (
                        id,
                        dpg.add_date_picker(
                            default_value={
                                "year": default_date.year - 1900,
                                "month": default_date.month - 1,
                                "month_day": default_date.day,
                            }
                        ),
                    )
                else:
                    return (id, dpg.add_date_picker())

        else:
            if isinstance(default_date, str):
                return self.add_input_text(
                    label,
                    default_date if default_date else "",
                    readonly,
                )
            return self.add_input_text(
                label,
                default_date.strftime("%d/%m/%Y") if default_date else "",
                readonly,
            )

    def add_date_picker_v2(self, label, default_date: date, readonly) -> ControlID:
        """Agrega un selector de fecha al formulario.
        Args:
            label: El texto de la etiqueta del campo.
            default_date: La fecha predeterminada para el selector de fecha.
            readonly: Un booleano que indica si el campo es de solo lectura.
        Returns:
            ControlID: Una tupla que contiene el ID del texto de la etiqueta y el ID del selector de fecha.
        """
        with dpg.group(horizontal=True):
            id = dpg.add_text(label)
            if default_date:
                return (
                    id,
                    dpg.add_input_text(default_value=default_date.strftime("%d/%m/%Y")),
                )
            else:
                return (id, dpg.add_input_text())
