from dataclasses import MISSING, Field, field
from enum import Enum, Flag, auto
from typing import Optional

ControlID = tuple[(int | str), (int | str)]

class SQLiteFieldConstraint(Flag):
    PRIMARY_KEY = auto()
    NOT_NULL = auto()
    AUTOINCREMENT = auto()
    UNIQUE = auto()
    NONE = auto()


class InputWidgetType(Enum):
    MODEL=auto()
    INPUT_TEXT = auto()
    INPUT_INT = auto()
    INPUT_FLOAT = auto()
    COMBO = auto()
    DATE_PICKER = auto()


# Constantes para las claves de metadatos del campo de diseño
CONTROL = "designer_control"
""" Tipo de control del campo, por ejemplo: InputText, InputInt, Combo, DatePicker """

TITLE = "designer_label"

""" Título del campo en el formulario, se usa para mostrar el nombre del campo """
READONLY = "designer_readonly"
""" Si el control es de solo lectura, no se puede editar el campo """

REQUIRED = "designer_required"
""" Este campo es obligatorio en el formulario """

ITEMS = "designer_items"
""" Items del Combobox o lista desplegable """

SEARCHABLE = "designer_searchable"
""" Permitir que el campo sea parte de un formulario de búsqueda """

SHOWINTABLE = "designer_showintable"
"""Permitir que la propiedad se muestre en el dataTable"""

SQLITE_FLAGS = "sqlite_flags"
""" Metadatos para restricciones de SQLite, como PRIMARY_KEY, AUTOINCREMENT, UNIQUE, NOT_NULL """

Empty = ""
""" Clase para representar un valor vacío, se usa para concatenar cadenas """


def flags(*, default,
          sqlite: SQLiteFieldConstraint,
          tcontrol: InputWidgetType,
          title: str = "",
          readonly: bool = False,
          required: bool = False,
          items: Optional[list] = None,
          searchable: bool = False, showintable:bool = True):
    """
    Decorador para definir metadatos de diseño para campos de dataclass.

    Parámetros:
        tcontrol (InputWidgetType): Tipo de control del campo.
        title (str): Título del campo en el formulario.
        readonly (bool): Si el campo es de solo lectura.
        required (bool): Si el campo es obligatorio.
        items (list): Lista de items para controles tipo Combo.
        searchable (bool): Si el campo es parte de un formulario de búsqueda.
    """

    return field(
        default=default,
        metadata={
            SQLITE_FLAGS: sqlite,
            CONTROL: tcontrol,
            TITLE: title,
            READONLY: readonly,
            REQUIRED: required,
            ITEMS: items or [],
            SEARCHABLE: searchable,
            SHOWINTABLE:showintable
        }
    )
