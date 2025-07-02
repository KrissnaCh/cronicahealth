from typing import Any
from database.crud import execute, execute_select, to_delete_sql, to_insert_sql, to_select_query, to_update_sql

from database.models import  InformacionGeneralPaciente
from internal import ActionDesigner
from ui.designer import  SearcherFlag
from ui.designer.detail import FormDetailDesigner
from ui.designer.frmtable import FormTableShow
import ui.message


def godjob():
    ui.message.show(
        "Informacion",
        "Todas las Operaciones Fueron Realizadas Con Exito...",
        ui.message.MessageBoxButtons.OK,
        None
    )


def error(error: Exception):
    ui.message.show(
        "Error",
        str(error),
        ui.message.MessageBoxButtons.OK,
        None
    )




class DbBasicComand(object):

    @staticmethod
    def ui_insert(old, new):
        try:
            execute(to_insert_sql(new))
            godjob()
        except Exception as e:
            error(e)
        pass

    @staticmethod
    def ui_delete(old, new):
        try:
            execute(to_delete_sql(new))
            godjob()
        except Exception as e:
            error(e)
        pass

    @staticmethod
    def ui_update(old, new):
        try:
            execute(to_update_sql(old, new))
            godjob()
        except Exception as e:
            error(e)
        pass
