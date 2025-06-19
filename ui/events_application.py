from database.crud import to_insert_sql
import ui.message

class DbEventPatient(object):

    @staticmethod
    def ui_insert(old, new):
        
        ui.message.show(
            "SQL Query",
            to_insert_sql(new),
            ui.message.MessageBoxButtons.OK, 
            None
        )
        pass

    @staticmethod
    def ui_delete(old, new):
        pass

    @staticmethod
    def ui_update(old, new):
        pass
