from dataclasses import field, fields, is_dataclass
from datetime import date
from enum import Flag, auto
import sqlite3
import internal
from typing import Any, Optional
from internal import SQLiteFieldConstraint, SQLITE_FLAGS
import json

def python_type_to_sqlite(py_type):
    if py_type == int or py_type == Optional[int]:
        return "INTEGER"
    elif py_type == float or py_type == Optional[float]:
        return "REAL"
    elif py_type == str or py_type == Optional[str]:
        return "TEXT"
    elif py_type == date or py_type == Optional[date]:
        return "INTEGER"  # Guardar fechas como texto
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
        # Ignorar campos con IGNORE
        """if SQLITE_FLAGS in f.metadata and SQLiteFieldConstraint.IGNORE in f.metadata[SQLITE_FLAGS]:
            continue"""
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
        # Ignorar campos con IGNORE
        """if SQLITE_FLAGS in f.metadata and SQLiteFieldConstraint.IGNORE in f.metadata[SQLITE_FLAGS]:
            continue"""
        isauto = SQLiteFieldConstraint.AUTOINCREMENT in f.metadata[SQLITE_FLAGS] and f.type == int
        if (isauto == False):
            col_names.append(f.name)
        value = getattr(instance, f.name)
        # Si es lista, serializar a JSON
        if isinstance(value, list):
            value = json.dumps(value)
            values.append(f"'{value.replace("'", "''")}'")
        # Formatea correctamente el valor para SQL
        elif isinstance(value, str):
            value = value.replace("'", "''")  # Escapa comillas simples
            values.append(f"'{value}'")  # Envuelve el valor entre comillas simples
        elif isinstance(value, date):
            values.append(f"{value.strftime('%Y%m%d')}")
        elif value is None:
            values.append("NULL")
        elif isauto:
            continue
        else:
            values.append(str(value))

    columns = ", ".join(col_names)
    values_clause = ", ".join(values)
    if use_reemplace:
        return f"INSERT OR REPLACE INTO {table_name} ({columns}) VALUES ({values_clause});"
    else:
        return f"INSERT INTO {table_name} ({columns}) VALUES ({values_clause});"
    

def to_update_sql(old: Any, new: Any) -> str:
    """
    Genera una sentencia UPDATE de SQLite para actualizar los valores de una fila,
    usando los campos de 'old' como filtro (WHERE) y los de 'new' como nuevos valores (SET).
    Ambos deben ser instancias del mismo dataclass.
    """
    if not (is_dataclass(old) and is_dataclass(new)):
        raise ValueError("Both old and new must be dataclass instances.")
    if type(old) != type(new):
        raise ValueError("Both dataclass instances must be of the same type.")

    table_name = type(old).__name__

    # Construir SET con los valores de 'new'
    set_clauses = []
    for f in fields(new):
        # Ignorar campos con IGNORE
        """if SQLITE_FLAGS in f.metadata and SQLiteFieldConstraint.IGNORE in f.metadata[SQLITE_FLAGS]:
            continue"""
        value = getattr(new, f.name)
        # Si es lista, serializar a JSON
        if isinstance(value, list):
            value_sql = f"'{json.dumps(value).replace("'", "''")}'"
        else:
            value_sql = __convert_value_sqlite(value)
        set_clauses.append(f'"{f.name}" = {value_sql}')
    set_clause = ", ".join(set_clauses)

    # Construir WHERE con los valores de 'old'
    where_clauses = []
    for f in fields(old):
        # Ignorar campos con IGNORE
        if SQLITE_FLAGS in f.metadata and SQLiteFieldConstraint.IGNORE in f.metadata[SQLITE_FLAGS]:
            continue
        value = getattr(old, f.name)
        value_sql = __convert_value_sqlite(value)
        where_clauses.append(f'"{f.name}" = {value_sql}')
    where_clause = " AND ".join(where_clauses)

    return f'UPDATE "{table_name}" SET {set_clause} WHERE {where_clause};'

def to_delete_sql(instance: Any) -> str:
    """
    Genera una sentencia DELETE de SQLite a partir de una instancia de dataclass.
    Si la tabla tiene clave primaria, usa los campos PRIMARY KEY como filtro.
    Si no tiene clave primaria, usa todos los campos con valor
    """
    table_type = type(instance)
    table_name = table_type.__name__
    if not is_dataclass(instance):
        raise ValueError("Input must be a dataclass instance.")

    # Buscar campos PRIMARY KEY
    pk_fields = []
    for f in fields(table_type):
        if SQLITE_FLAGS in f.metadata and SQLiteFieldConstraint.PRIMARY_KEY in f.metadata[SQLITE_FLAGS]:
            pk_fields.append(f)

    filters = []

    if pk_fields:
        # Usar solo los campos PRIMARY KEY
        for f in pk_fields:
            # Ignorar campos con IGNORE
            """if SQLITE_FLAGS in f.metadata and SQLiteFieldConstraint.IGNORE in f.metadata[SQLITE_FLAGS]:
                continue"""
            value = getattr(instance, f.name)
            # Si es lista, serializar a JSON
            if isinstance(value, list):
                value = f"'{json.dumps(value).replace("'", "''")}'"
            else:
                value = __convert_value_sqlite(value)
            filters.append(f'"{f.name}" = {value}')
            
            
    else:
        # Usar todos los campos con valor distinto de None
        for f in fields(instance):
            # Ignorar campos con IGNORE
            """if SQLITE_FLAGS in f.metadata and SQLiteFieldConstraint.IGNORE in f.metadata[SQLITE_FLAGS]:
                continue"""
            value = getattr(instance, f.name)
            # Si es lista, serializar a JSON
            if isinstance(value, list):
                value = f"'{json.dumps(value).replace("'", "''")}'"
            else:
                value = __convert_value_sqlite(value)
            filters.append(f'"{f.name}" = {value}')
                

    if not filters:
        raise ValueError("No fields to filter on for DELETE statement.")

    where_clause = " AND ".join(filters)
    query = f'DELETE FROM "{table_name}" WHERE {where_clause};'
    return query

def __convert_value_sqlite(value):
    if isinstance(value, str):
        value = value.replace("'", "''") 
        value = f"'{value}'"
    elif isinstance(value, date):
        value=f"{value.strftime('%Y%m%d')}"
    elif value is None:
        value= "NULL"
    else:
        value= str(value)
    return value

def to_select_query(instance, table_name=None, ignore_primary_int=False, comparator="=", limit_start=None, limit_end=None):
    """
    Genera una consulta SELECT de SQLite utilizando los atributos con valor distinto de None de una instancia de dataclass como filtros.
    
    Parámetros:
        instance: instancia del dataclass que se usará para los valores de filtro.
        table_name: opcionalmente, permite sobrescribir el nombre de la tabla (por defecto es el nombre de la clase).
        comparator: comparador SQL a utilizar (por defecto "="). Puede personalizarse por campo si es necesario.
        limit_start: índice inicial para LIMIT/OFFSET (opcional).
        limit_end: cantidad de filas a devolver (opcional).
    
    Retorna:
        Una tupla con (cadena de consulta, lista de parámetros) para uso seguro con sqlite3.
    """
    if not is_dataclass(instance):
        raise ValueError("Input must be a dataclass instance.")

    table_name = table_name or type(instance).__name__
    filters = []
    params = []

    for f in fields(instance):
        # Ignorar campos con IGNORE
        """if SQLITE_FLAGS in f.metadata and SQLiteFieldConstraint.IGNORE in f.metadata[SQLITE_FLAGS]:
            continue"""
        value = getattr(instance, f.name)
        # Ignore primary key fields of type int if ignore_primary_int is True
        is_primary_int = (
            SQLITE_FLAGS in f.metadata and
            SQLiteFieldConstraint.PRIMARY_KEY in f.metadata[SQLITE_FLAGS] and
            f.type == int
        )
        if value is not None:
            if ignore_primary_int and is_primary_int:
                continue
            filters.append(f'"{f.name}" {comparator} ?')
            params.append(value)

    where_clause = ""
    if filters:
        where_clause = " WHERE " + " AND ".join(filters)

    limit_clause = ""
    # Solo agrega LIMIT si alguno de los parámetros está definido
    if limit_start is not None and limit_end is not None:
        limit_clause = f" LIMIT ? OFFSET ?"
        params.extend([limit_end, limit_start])
    elif limit_end is not None:
        limit_clause = f" LIMIT ?"
        params.append(limit_end)
    # Si ambos son None, no se agrega LIMIT

    query = f'SELECT * FROM "{table_name}"{where_clause}{limit_clause};'
    return query, params



def execute(query:str)->None:
    sqlite_database = sqlite3.connect("database.sqlite")
    sqlite_database.execute(query)
    sqlite_database.commit()
    sqlite_database.close()
    del sqlite_database


def execute_select(dataclass_type:type, query: str, callback, params=None):
    """
    Ejecuta una consulta SELECT en la base de datos SQLite y llama al callback por cada fila leída.

    Args:
        query (str): Consulta SQL SELECT a ejecutar.
        callback (callable): Función a invocar por cada fila, recibe los valores de la fila como argumentos.
        params (list/tuple, opcional): Parámetros para la consulta SQL (para evitar inyección SQL).

    Returns:
        None
    """
    conn = sqlite3.connect("database.sqlite")
    cursor = conn.cursor()
    if params is None:
        cursor.execute(query)
    else:
        cursor.execute(query, params)
    for row in cursor:
        callback(__tuple_to_dataclass(dataclass_type,row))
    cursor.close()
    conn.close()

def __tuple_to_dataclass(dataclass_type:type, data_tuple)->Any:
    """
    Convierte una tupla de valores en una instancia del dataclass especificado.
    El orden de los elementos de la tupla debe coincidir con el orden de los campos del dataclass.

    Args:
        dataclass_type: Clase del dataclass destino.
        data_tuple: Tupla con los valores.

    Returns:
        Instancia del dataclass con los valores asignados.
    """
    if not is_dataclass(dataclass_type):
        raise ValueError("dataclass_type must be a dataclass.")
    field_types = [f.type for f in fields(dataclass_type)]
    values = []
    for value, ftype in zip(data_tuple, field_types):
        if ftype == date or ftype == Optional[date]:
            # Intenta parsear fechas en formato YYYYMMDD
            value = str(value)
            try:
                value = date(int(value[:4]), int(value[4:6]), int(value[6:8]))
            except Exception:
                pass
        elif ftype == list or getattr(ftype, "__origin__", None) == list:
            # Deserializar JSON a lista
            try:
                value = json.loads(value) if value is not None else []
            except Exception:
                value = []
        values.append(value)
    return dataclass_type(*values)

def make_database(instances:list):
    """
    Crea una base de datos SQLite a partir de un conjunto de clases dataclass, 
    generando las tablas correspondientes automáticamente.

    Parámetros:
        instances(list): Instancias tipo dataclass que se usaran para crear las tablas de datos

    Funcionamiento:
        - Define una lista de clases dataclass (`instances`) que representan los modelos de datos.
        - Abre una conexión a la base de datos SQLite en la ruta especificada.
        - Para cada clase en la lista:
            - Se genera la sentencia SQL de creación de tabla usando `create_table_sql(instance)`.
            - Se ejecuta la sentencia SQL para crear la tabla si no existe.
            - Si ocurre un error durante la creación de la tabla, imprime el error y la sentencia SQL fallida para ayudar en la depuración.
    """
    
    for instance in instances:
        try:
            execute(create_table_sql(instance))
        except Exception as e:
            print(f"{instance}: {e}")