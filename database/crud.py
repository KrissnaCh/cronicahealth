from dataclasses import field, fields, is_dataclass
from datetime import date
from enum import Flag, auto
from typing import Any
from internal import SQLiteP

def python_type_to_sqlite(py_type):
    if py_type == int:
        return "INTEGER"
    elif py_type == float:
        return "REAL"
    elif py_type == str:
        return "TEXT"
    elif py_type == date:
        return "TEXT"  # Guardar fechas como texto
    else:
        return "TEXT"  # Default

def create_table_sql(dataclass_type):
    """columnas de datos"""
    columns = []
    """solo puede haber un auto increment y una sola primary key"""
    primarykey = []
    autoincrement=[]
    for f in fields(dataclass_type):
        col_type = python_type_to_sqlite(f.type)
        col_def = f"\"{f.name}\" {col_type}"
        if f.metadata.__contains__(SQLiteP):
            if SQLiteFieldConstraint.PRIMARY_KEY in f.metadata[SQLiteP] :
                primarykey.append(f'"{f.name}"')
            if SQLiteFieldConstraint.AUTOINCREMENT in f.metadata[SQLiteP] and len(autoincrement)==0:
                autoincrement.append(f'"{f.name}"')
            if SQLiteFieldConstraint.UNIQUE in f.metadata[SQLiteP]:
                col_def += " UNIQUE "
            if SQLiteFieldConstraint.NOT_NULL in f.metadata[SQLiteP]:
                col_def += " NOT NULL "

        columns.append(col_def)
    columns_sql = ", ".join(columns)
    table_name = dataclass_type.__name__
    """condicionales con el fin de cumplir con los estandares de sqlite"""
    if len(primarykey) == 0 and len(autoincrement) == 0:
        """tabla basica"""
        return f"CREATE TABLE IF NOT EXISTS '{table_name}' ({columns_sql});"
    else:
        if len(autoincrement) ==1 :
            """tiene que ser misma primary key"""
            return f"CREATE TABLE IF NOT EXISTS '{table_name}' ({columns_sql},PRIMARY KEY({autoincrement[0]} AUTOINCREMENT));"
        else:
            """todas las primary key pero no puede haber un autoincrement"""
            return f"CREATE TABLE IF NOT EXISTS '{table_name}' ({columns_sql},PRIMARY KEY({",".join(primarykey)}));"
        
def to_insert_sql(instance: Any, use_reemplace:bool = False) -> str:
    """
        Genera una sentencia INSERT de SQLite a partir de una instancia de dataclass.

        Esta función toma un objeto dataclass y construye dinámicamente una consulta SQL INSERT 
        validando primero que la entrada sea una instancia válida de dataclass. Es útil para 
        mapear objetos Python a registros de base de datos de forma estructurada y segura.

        Args:
            instance: Objeto dataclass con los datos a insertar

        Raises:
            ValueError: Si el objeto no es una instancia de dataclass

        Returns:
            str: Sentencia SQL INSERT con los campos del dataclass
    """
    table_name = type(instance).__name__
    if not is_dataclass(instance):
        raise ValueError("Input must be a dataclass instance.")

    col_names = []
    values = []

    for f in fields(instance):
        col_names.append(f.name)
        value = getattr(instance, f.name)
        # Formatea correctamente el valor para SQL
        if isinstance(value, str):
            value = value.replace("'", "''")  # Escapa comillas simples
            values.append(f"'{value}'")  # Envuelve el valor entre comillas simples
        elif isinstance(value, date):
            values.append(f"{value.strftime("%Y%m%d")}")
        elif value is None:
            values.append("NULL")
        else:
            values.append(str(value))

    columns = ", ".join(col_names)
    values_clause = ", ".join(values)
    if use_reemplace:
        return f"INSERT OR REPLACE INTO {table_name} ({columns}) VALUES ({values_clause});"
    else:
        return f"INSERT INTO {table_name} ({columns}) VALUES ({values_clause});"

class SQLiteFieldConstraint(Flag):
    PRIMARY_KEY =auto()
    NOT_NULL =auto()
    AUTOINCREMENT =auto()
    UNIQUE =auto()
    NONE=auto()

