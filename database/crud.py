from dataclasses import field, fields, is_dataclass
from datetime import date
from enum import Flag, auto
from typing import Any
from internal import SQLiteFieldConstraint, SQLITE_FLAGS

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
    """
    Genera un comando SQL para crear una tabla SQLite a partir de un dataclass Python.
    
    Explicación:
    -----------------------------------------
    Esta función toma un tipo de dataclass y construye la instrucción SQL correspondiente para crear la tabla en SQLite.
    Extrae los metadatos de los campos del dataclass para determinar los tipos de columna y restricciones como PRIMARY KEY, AUTOINCREMENT, UNIQUE y NOT NULL.

    Consideraciones importantes:
    - Solo puede existir una columna AUTOINCREMENT y debe ser PRIMARY KEY (esto es una restricción de SQLite).
    - Se puede definir una PRIMARY KEY compuesta, pero en ese caso ninguna columna puede ser AUTOINCREMENT.
    - Los metadatos se leen desde el parámetro 'metadata' de cada campo, usando la clave 'SQLITE_FLAGS' y las constantes de SQLiteFieldConstraint.
    - Si no se define ninguna PRIMARY KEY, la tabla será básica sin clave primaria.
    - Si hay una columna AUTOINCREMENT, se asegura que sea la única PRIMARY KEY.
    - Si hay varias columnas PRIMARY KEY pero ninguna AUTOINCREMENT, se crea una clave primaria compuesta.

    Requisitos para los campos del dataclass:
    - Los tipos Python deben poder mapearse a tipos SQLite (usa la función python_type_to_sqlite).
    - Para utilizar restricciones, hay que emplear el argumento 'metadata' en los campos del dataclass.
    """

    columns = []      # Lista de definiciones de columnas (nombre y tipo + restricciones)
    primarykey = []   # Almacena los nombres de los campos PRIMARY KEY
    autoincrement = []# Almacena el campo que será AUTOINCREMENT, si existe

    for f in fields(dataclass_type):
        # Determina el tipo SQLite basado en el tipo Python del campo
        col_type = python_type_to_sqlite(f.type)
        col_def = f"\"{f.name}\" {col_type}"

        # Procesa metadatos para restricciones específicas
        if f.metadata.__contains__(SQLITE_FLAGS):
            # PRIMARY KEY
            if SQLiteFieldConstraint.PRIMARY_KEY in f.metadata[SQLITE_FLAGS]:
                primarykey.append(f'"{f.name}"')
            # AUTOINCREMENT (solo una columna puede tenerlo)
            if SQLiteFieldConstraint.AUTOINCREMENT in f.metadata[SQLITE_FLAGS] and len(autoincrement) == 0:
                autoincrement.append(f'"{f.name}"')
            # UNIQUE
            if SQLiteFieldConstraint.UNIQUE in f.metadata[SQLITE_FLAGS]:
                col_def += " UNIQUE "
            # NOT NULL
            if SQLiteFieldConstraint.NOT_NULL in f.metadata[SQLITE_FLAGS]:
                col_def += " NOT NULL "

        columns.append(col_def)

    columns_sql = ", ".join(columns)
    table_name = dataclass_type.__name__

    # Condicionales para construir la instrucción SQL respetando las reglas de SQLite
    if len(primarykey) == 0 and len(autoincrement) == 0:
        # Caso sin clave primaria ni autoincrement: tabla básica
        return f"CREATE TABLE IF NOT EXISTS '{table_name}' ({columns_sql});"
    else:
        if len(autoincrement) == 1:
            # Caso con AUTOINCREMENT: debe ser la única PRIMARY KEY
            return f"CREATE TABLE IF NOT EXISTS '{table_name}' ({columns_sql}, PRIMARY KEY({autoincrement[0]} AUTOINCREMENT));"
        else:
            # Caso de clave primaria compuesta, sin autoincrement
            return f"CREATE TABLE IF NOT EXISTS '{table_name}' ({columns_sql}, PRIMARY KEY({', '.join(primarykey)}));"
        
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
    
def to_select_query(instance, table_name=None, comparator="="):
    """
    Genera una consulta SELECT de SQLite utilizando los atributos con valor distinto de None de una instancia de dataclass como filtros.
    
    Parámetros:
        instance: instancia del dataclass que se usará para los valores de filtro.
        table_name: opcionalmente, permite sobrescribir el nombre de la tabla (por defecto es el nombre de la clase).
        comparator: comparador SQL a utilizar (por defecto "="). Puede personalizarse por campo si es necesario.
    
    Retorna:
        Una tupla con (cadena de consulta, lista de parámetros) para uso seguro con sqlite3.
    """
    if not is_dataclass(instance):
        raise ValueError("Input must be a dataclass instance.")

    table_name = table_name or type(instance).__name__
    filters = []
    params = []

    for f in fields(instance):
        value = getattr(instance, f.name)
        if value is not None:
            filters.append(f'"{f.name}" {comparator} ?')
            params.append(value)

    where_clause = ""
    if filters:
        where_clause = " WHERE " + " AND ".join(filters)

    query = f'SELECT * FROM "{table_name}"{where_clause};'
    return query, params



