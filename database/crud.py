from dataclasses import field, fields
from datetime import date
from enum import Flag, auto
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
        

class SQLiteFieldConstraint(Flag):
    PRIMARY_KEY =auto()
    NOT_NULL =auto()
    AUTOINCREMENT =auto()
    UNIQUE =auto()
    NONE=auto()

