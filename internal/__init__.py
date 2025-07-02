from dataclasses import MISSING, Field, field
from enum import Enum, Flag, auto
import sqlite3
from typing import Callable, Optional, TypeAlias

ControlID: TypeAlias = tuple[(int | str), (int | str)]

ActionDesigner: TypeAlias = Optional[Callable]


class SQLiteFieldConstraint(Flag):
    PRIMARY_KEY = auto()
    NOT_NULL = auto()
    AUTOINCREMENT = auto()
    UNIQUE = auto()
    NONE = auto()
    IGNORE = auto()


class InputWidgetType(Enum):
    MODEL = auto()
    NONE = auto()
    SEP = auto()
    INPUT_JSON = auto()
    INPUT_TEXT = auto()
    INPUT_TEXT_RICH = auto()
    INPUT_INT = auto()
    INPUT_FLOAT = auto()
    COMBO = auto()
    LIST = auto()
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

LISTMODEL = "designer_model"
""" Modelo de datos asociado al campo, se usa para campos tipo lista """


def flags(
    *,
    default,
    sqlite: SQLiteFieldConstraint,
    tcontrol: InputWidgetType,
    default_factory=None,
    title: str = "",
    readonly: bool = False,
    required: bool = False,
    items: Optional[list] = None,
    searchable: bool = False,
    showintable: bool = True
):
    """
    Crea un campo personalizado para modelos de datos, agregando metadatos útiles para integración con SQLite y widgets de entrada.
    Parámetros:
        default: Valor por defecto del campo.
        sqlite (SQLiteFieldConstraint): Restricciones o configuración específica para el campo en SQLite.
        tcontrol (InputWidgetType): Tipo de widget de entrada asociado al campo.
        default_factory (opcional): Función para generar el valor por defecto dinámicamente.
        title (str, opcional): Título descriptivo del campo. Por defecto es una cadena vacía.
        readonly (bool, opcional): Indica si el campo es de solo lectura. Por defecto es False.
        required (bool, opcional): Indica si el campo es obligatorio. Por defecto es False.
        items (list, opcional): Lista de opciones para campos tipo selección. Por defecto es None.
        searchable (bool, opcional): Indica si el campo es buscable. Por defecto es False.
        showintable (bool, opcional): Indica si el campo se muestra en tablas. Por defecto es True.
    Retorna:
        Un campo configurado con los metadatos especificados, listo para ser usado en modelos de datos.
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
            SHOWINTABLE: showintable,
        },
    )


def flagsv2(
    *,
    default_factory,
    model,
    sqlite: SQLiteFieldConstraint,
    tcontrol: InputWidgetType,
    title: str = "",
    readonly: bool = False,
    required: bool = False,
    items: Optional[list] = None,
    searchable: bool = False,
    showintable: bool = True
):
    """
    Crea un campo personalizado para modelos de datos, agregando metadatos útiles para integración con SQLite y widgets de entrada.
    Parámetros:
        sqlite (SQLiteFieldConstraint): Restricciones o configuración específica para el campo en SQLite.
        tcontrol (InputWidgetType): Tipo de widget de entrada asociado al campo.
        default_factory (opcional): Función para generar el valor por defecto dinámicamente.
        title (str, opcional): Título descriptivo del campo. Por defecto es una cadena vacía.
        readonly (bool, opcional): Indica si el campo es de solo lectura. Por defecto es False.
        required (bool, opcional): Indica si el campo es obligatorio. Por defecto es False.
        items (list, opcional): Lista de opciones para campos tipo selección. Por defecto es None.
        searchable (bool, opcional): Indica si el campo es buscable. Por defecto es False.
        showintable (bool, opcional): Indica si el campo se muestra en tablas. Por defecto es True.
    Retorna:
        Un campo configurado con los metadatos especificados, listo para ser usado en modelos de datos.
    """
    return field(
        default_factory=default_factory,
        metadata={
            SQLITE_FLAGS: sqlite,
            CONTROL: tcontrol,
            TITLE: title,
            READONLY: readonly,
            REQUIRED: required,
            ITEMS: items or [],
            SEARCHABLE: searchable,
            SHOWINTABLE: showintable,
            LISTMODEL:model
        },
    )


def is_empty_or_whitespace(s):
    return not s or s.strip() == ""
