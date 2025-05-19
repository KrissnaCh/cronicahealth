#import database
import dearpygui.dearpygui as dpg

import database.crud
import database.models


if __name__ == "__main__":
    print(database.crud.create_table_sql(database.models.InformacionGeneralPaciente))
    pass