from dataclasses import fields, is_dataclass
from datetime import date
from enum import Enum, auto
from typing import Any, Callable, Optional, Union
import dearpygui.dearpygui as dpg
from database import crud
from internal import (
    CONTROL,
    ITEMS,
    READONLY,
    REQUIRED,
    SEARCHABLE,
    SHOWINTABLE,
    TITLE,
    ActionDesigner,
    ControlID,
    Empty,
    InputWidgetType,
    is_empty_or_whitespace,
)
from internal.ext import align_items
import copy
import ui.message as msgbox
from ui.message import MessageBoxButtons

window_count = 0
window_base_x = 10  # posición X fija
window_base_y = 50  # posición Y inicial
window_spacing = 50  # distancia vertical entre ventanas


class SearcherFlag(Enum):
    INSERT = auto()
    UPDATE = auto()
    DELETE = auto()
    CONSULT = auto()


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

    def show(self):
        """Muestra la ventana del formulario de detalle."""
        dpg.show_item(self._window_id)

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
        global window_count
        y_pos = window_base_y + window_count * window_spacing
        x_pos = window_base_x + window_count * window_spacing
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
                    dt[last].append(f)

            for key in dt:
                self.builder.add_separator(key)

                for chunk in batched(dt[key], 2):
                    with dpg.group(horizontal=True):
                        for f in chunk:
                            self.makecontrol(just, f)

            """fields_compatible = []
            tmp = []
            for f in __fields:
                if f.metadata[CONTROL] == InputWidgetType.SEP:
                    fields_compatible.append(tmp)
                    tmp = []
                else:
                    tmp.append(f)"""

            # for chunk in batched(__fields,2):
            # for chunk in batched(ls,2):
            # with dpg.group(horizontal=True):
            #        print("--")
            #        for f in chunk:
            # self.makecontrol(just, f)
            #            print(f.metadata[TITLE])

            """for chunk in batched(fields_compatible,2):
                with dpg.group(horizontal=True):
                    for f in chunk:
                        #if all(key in f.metadata for key in self.designer_fields):
                        self.makecontrol(just, f)"""

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
                        dpg.add_button(
                            label="Guardar",
                            callback=self.__btn_callback,
                            user_data=self._save_callback,
                        )
                    if self._update_callback:
                        dpg.add_button(
                            label="Actualizar",
                            callback=self.__btn_callback,
                            user_data=self._update_callback,
                        )
                    if self._delete_callback:
                        dpg.add_button(
                            label="Eliminar",
                            callback=self.__btn_callback,
                            user_data=self._delete_callback,
                        )
        window_count = (window_count + 1) % 10
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


class DesignerBuilder:
    """Clase para construir controles de formulario de manera sencilla."""

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
        global window_count
        y_pos = window_base_y + window_count * window_spacing
        x_pos = window_base_x + window_count * window_spacing
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
                    dpg.add_button(label="Buscar", callback=self.__search)

        window_count = (window_count + 1) % 10
        pass


class FormTableShow:
    def __show_selection(self, sender):
        self.close()
        if self._current_model:
            if self._custom_show:
                self._custom_show(self._current_model, self._title, self._args)
                pass
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

    def __row_clicked(self, sender, value, user_data):
        """Maneja el evento de selección de una fila en la tabla."""
        if value:
            rowid, data = user_data
            for rid, selectables in self._ids_table.items():
                if rid != rowid:
                    for selectable in selectables:
                        dpg.set_value(selectable, False)
            self._current_model = data

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
        self._window_id: Union[int, str] = None  # type: ignore
        self._current_model: Optional[object] = None
        self._num_columns = sum(
            1
            for f in fields(self._model)
            if all(key in f.metadata for key in self._designer_fields)
            and f.metadata[SHOWINTABLE]
        )
        self._ids_table: dict[int | str, list] = {}
        self.__create_ui()

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

    def __create_ui(self):
        global window_count
        y_pos = window_base_y + window_count * window_spacing
        x_pos = window_base_x + window_count * window_spacing
        with dpg.window(
            label="Tabla de " + self._title,
            pos=(x_pos, y_pos),
            no_collapse=True,
            show=False,
        ) as self._window_id:
            dpg.add_button(label="Mostrar Seleccion", callback=self.__show_selection)
            with dpg.table(
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
        pass

    def show(self):
        dpg.show_item(self._window_id)

    def close(self):
        dpg.delete_item(self._window_id)
