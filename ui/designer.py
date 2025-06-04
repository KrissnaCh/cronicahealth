from dataclasses import fields, is_dataclass
from datetime import date
from enum import Enum, auto
from typing import Union
import dearpygui.dearpygui as dpg
from internal import CONTROL, ITEMS, READONLY, REQUIRED, SEARCHABLE, TITLE, ControlID, Empty, InputWidgetType
from internal.ext import align_items

window_count = 0
window_base_x = 10  # posición X fija
window_base_y = 50  # posición Y inicial
window_spacing = 50 # distancia vertical entre ventanas

class FormDetailDesigner:
    def show(self):
        """Muestra la ventana del formulario de detalle."""
        dpg.show_item(self._window_id)

    def __init__(self, model, title: str, save_callback=None, update_callback=None, delete_callback=None, closeonexec=True):
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
        self.designer_fields = [CONTROL, TITLE,
                                READONLY, REQUIRED, ITEMS, SEARCHABLE]

        # callbacks para guardar, actualizar y eliminar
        self._save_callback = save_callback
        self._update_callback = update_callback
        self._delete_callback = delete_callback

        # Indica si se debe cerrar la ventana al ejecutar una acción.
        self._closeonexec = closeonexec

        self.model_type = type(model)
        self.builder = DesignerBuilder()

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
        
        with dpg.window(label=self._title, autosize=True,pos=(x_pos, y_pos), no_collapse=True, show=False) as self._window_id:
            # Calcula la longitud máxima de las etiquetas para la alineación, usando una expresión generadora para eficiencia
            just = max((len(f.metadata[TITLE]) for f in fields(self.model)
                        if all(key in f.metadata for key in self.designer_fields)), default=0)
            for f in fields(self.model):
                if all(key in f.metadata for key in self.designer_fields):
                    match f.metadata[CONTROL]:
                        case InputWidgetType.INPUT_INT:
                            self.builder.add_input_int(self.mark_required(
                                f.metadata[TITLE],  f.metadata[REQUIRED]).ljust(just), getattr(self.model, f.name),  f.metadata[READONLY])
                            pass
                        case InputWidgetType.INPUT_TEXT:
                            self.builder.add_input_text(self.mark_required(
                                f.metadata[TITLE], f.metadata[REQUIRED]).ljust(just), getattr(self.model, f.name), f.metadata[READONLY])
                            pass
                        case InputWidgetType.INPUT_FLOAT:
                            self.builder.add_input_float(self.mark_required(
                                f.metadata[TITLE], f.metadata[REQUIRED]).ljust(just), getattr(self.model, f.name), f.metadata[READONLY])
                            pass
                        case InputWidgetType.DATE_PICKER:
                            self.builder.add_date_picker(self.mark_required(
                                f.metadata[TITLE], f.metadata[REQUIRED]).ljust(just), getattr(self.model, f.name), f.metadata[READONLY])
                        case InputWidgetType.COMBO:
                            self.builder.add_combo(self.mark_required(
                                f.metadata[TITLE], f.metadata[REQUIRED]).ljust(just), f.metadata[ITEMS], getattr(self.model, f.name), f.metadata[READONLY])
                        case _:
                            pass

            count_callbacks = sum(
                cb is not None for cb in [
                    self._save_callback,
                    self._update_callback,
                    self._delete_callback
                ]
            )
            if count_callbacks > 0:
                dpg.add_separator()

                with align_items(0, count_callbacks):  # Alinea los botones a la derecha
                    if self._save_callback:
                        dpg.add_button(
                            label="Guardar", callback=self._save_callback, user_data=self.model)
                    if self._update_callback:
                        dpg.add_button(
                            label="Actualizar", callback=self._update_callback, user_data=self.model)
                    if self._delete_callback:
                        dpg.add_button(
                            label="Eliminar", callback=self._delete_callback, user_data=self.model)
        window_count = (window_count + 1) % 10
        pass


class DesignerBuilder:
    """Clase para construir controles de formulario de manera sencilla."""

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
            return (id, dpg.add_input_text(
                default_value=default_value if default_value else "", readonly=_readonly
            ))

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
                return (id, dpg.add_input_int(
                    default_value=default_value if default_value else 0,
                    min_value=0,
                    min_clamped=True
                ))
        else:
            return self.add_input_text(label, str(default_value), _readonly)

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
                return (id, dpg.add_input_float(
                    default_value=default_value if default_value else 0,
                    min_value=0,
                    min_clamped=True,
                    readonly=_readonly
                ))

        else:
            return self.add_input_text(label, str(default_value), _readonly)

    def add_combo(self, label,  items, default_value, readonly) -> ControlID:
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
                return (id, dpg.add_combo(
                    items=items,
                    default_value=default_value if default_value else ""
                ))
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
                    return (id, dpg.add_date_picker(
                        default_value={
                            'year': default_date.year-1900,
                            'month': default_date.month-1,
                            'month_day': default_date.day
                        }
                    ))
                else:
                    return (id, dpg.add_date_picker())

        else:
            return self.add_input_text(label, default_date.strftime("%d/%m/%Y") if default_date else "", readonly)


class SearcherFlag(Enum):
    UPDATE = auto()
    DELETE = auto()
    CONSULT = auto()


class FormSearcherDesigner:
    def show(self):
        """Muestra la ventana del formulario de detalle."""
        dpg.show_item(self._window_id)
        for i in range(0, 4):
            with dpg.table_row(parent=self._table_id):
                for f in fields(self.model):
                    if all(key in f.metadata for key in self.designer_fields):
                        dpg.add_text(f"")

    def __init__(self, model, title: str, flag: SearcherFlag = SearcherFlag.CONSULT):
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
        self._table_id: Union[int, str] = 0
        """ ID de la tabla para referencia futura."""
        self.model = model
        self._title = title
        self.designer_fields = [CONTROL, TITLE,
                                READONLY, ITEMS, SEARCHABLE]

        self.flag = flag
        """Tipo de acciones que se pueden realizar en el formulario, por ejemplo: Actualizar, Eliminar, Consultar"""

        self.model_type = type(model)
        self.builder = DesignerBuilder()

        self.__create_ui()

    def __create_ui(self):
        global window_count
        y_pos = window_base_y + window_count * window_spacing
        x_pos = window_base_x + window_count * window_spacing
        """Crea la interfaz de usuario del formulario de detalle."""
        # Genera un ID único para la ventana
        with dpg.window(label=self._title, autosize=True,pos=(x_pos, y_pos), no_collapse=True, show=False) as self._window_id:
            # Calcula la longitud máxima de las etiquetas para la alineación, usando una expresión generadora para eficiencia
            just = max((len(f.metadata[TITLE]) for f in fields(self.model)
                        if all(key in f.metadata for key in self.designer_fields)), default=0)
            for f in fields(self.model):
                if all(key in f.metadata for key in self.designer_fields):
                    if f.metadata[SEARCHABLE] == False:
                        continue
                    match f.metadata[CONTROL]:
                        case InputWidgetType.INPUT_INT:
                            self.builder.add_input_int(f.metadata[TITLE].ljust(
                                just), getattr(self.model, f.name),  f.metadata[READONLY])
                            pass
                        case InputWidgetType.INPUT_TEXT:
                            self.builder.add_input_text(f.metadata[TITLE].ljust(
                                just), getattr(self.model, f.name), f.metadata[READONLY])
                            pass
                        case InputWidgetType.INPUT_FLOAT:
                            self.builder.add_input_float(f.metadata[TITLE].ljust(
                                just), getattr(self.model, f.name), f.metadata[READONLY])
                            pass
                        case InputWidgetType.DATE_PICKER:
                            self.builder.add_date_picker(f.metadata[TITLE].ljust(
                                just), getattr(self.model, f.name), f.metadata[READONLY])
                        case InputWidgetType.COMBO:
                            self.builder.add_combo(f.metadata[TITLE].ljust(
                                just), f.metadata[ITEMS], getattr(self.model, f.name), f.metadata[READONLY])
                        case _:
                            pass
            dpg.add_separator()
            with dpg.table()as self._table_id:
                for f in fields(self.model):
                    if all(key in f.metadata for key in self.designer_fields):
                        dpg.add_table_column(label=f.metadata[TITLE])
        window_count = (window_count + 1) % 10
        pass

