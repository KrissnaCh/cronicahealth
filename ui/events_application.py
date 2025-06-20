from typing import Any
from database.crud import execute, execute_select, to_delete_sql, to_insert_sql, to_select_query, to_update_sql

from database.models import AntecedentesFamiliares, AntecedentesPersonales, ExamenFisico, ExamenFisicoPorSistemas, InformacionGeneralPaciente, PlanManejo, Profesional, Seguimiento
from internal import ActionDesigner
from ui.designer import FormDetailDesigner, FormTableShow, SearcherFlag
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


class DbEventAntecedentesPersonales(object):
    @staticmethod
    def ui_insert(orig: InformacionGeneralPaciente, old: AntecedentesPersonales, new: AntecedentesPersonales):
        try:
            new.id = orig.id
            execute(to_insert_sql(new))
            godjob()
        except Exception as e:
            error(e)
        pass

    @staticmethod
    def ui_custom_show(current_model: InformacionGeneralPaciente, title: str, args: tuple[SearcherFlag, ActionDesigner]):
        foud = False

        def show_data(data):
            nonlocal foud
            foud = True
            match args[0]:
                case SearcherFlag.UPDATE:
                    FormDetailDesigner(data, title=f"Actualizar Datos de {current_model.nombre_completo}",
                                       update_callback=args[1]).show()

                case SearcherFlag.CONSULT:
                    FormDetailDesigner(data, title=f"Consultar Datos de {current_model.nombre_completo}",
                                       is_readonly=True).show()

                case SearcherFlag.DELETE:
                    FormDetailDesigner(
                        data, title=f"Eliminar Datos de {current_model.nombre_completo}", delete_callback=args[1], is_readonly=True).show()

        search = AntecedentesPersonales()
        search.id = current_model.id
        query, params = to_select_query(search, limit_end=1)
        execute_select(AntecedentesPersonales, query, show_data, params)
        if foud == False:
            ui.message.show(
                "Error",
                f"Datos no Encontrados de \"{current_model.nombre_completo}\"",
                ui.message.MessageBoxButtons.OK,
                None
            )

class DbEventAntecedentesFamiliares(object):
    @staticmethod
    def ui_insert(orig: InformacionGeneralPaciente, old: AntecedentesFamiliares, new: AntecedentesFamiliares):
        try:
            new.id = orig.id
            execute(to_insert_sql(new))
            godjob()
        except Exception as e:
            error(e)
        pass

    @staticmethod
    def ui_custom_show(current_model: InformacionGeneralPaciente, title: str, args: tuple[SearcherFlag, ActionDesigner]):
        foud = False

        def show_data(data):
            nonlocal foud
            foud = True
            match args[0]:
                case SearcherFlag.UPDATE:
                    FormDetailDesigner(data, title=f"Actualizar Datos de {current_model.nombre_completo}",
                                       update_callback=args[1]).show()

                case SearcherFlag.CONSULT:
                    FormDetailDesigner(data, title=f"Consultar Datos de {current_model.nombre_completo}",
                                       is_readonly=True).show()

                case SearcherFlag.DELETE:
                    FormDetailDesigner(
                        data, title=f"Eliminar Datos de {current_model.nombre_completo}", delete_callback=args[1], is_readonly=True).show()

        search = AntecedentesFamiliares()
        search.id = current_model.id
        query, params = to_select_query(search, limit_end=1)
        execute_select(AntecedentesFamiliares, query, show_data, params)
        if foud == False:
            ui.message.show(
                "Error",
                f"Datos no Encontrados de \"{current_model.nombre_completo}\"",
                ui.message.MessageBoxButtons.OK,
                None
            )

class DbEventExamenFisicoPorSistemas(object):
    
    @staticmethod
    def ui_insert(orig: InformacionGeneralPaciente, old: ExamenFisicoPorSistemas, new: ExamenFisicoPorSistemas):
        try:
            new.id = orig.id
            execute(to_insert_sql(new))
            godjob()
        except Exception as e:
            error(e)
        pass

    @staticmethod
    def ui_custom_show(current_model: InformacionGeneralPaciente, title: str, args: tuple[SearcherFlag, ActionDesigner]):
        foud = False

        def show_data(data):
            nonlocal foud
            foud = True
            match args[0]:
                case SearcherFlag.UPDATE:
                    FormDetailDesigner(data, title=f"Actualizar Datos de {current_model.nombre_completo}",
                                       update_callback=args[1]).show()

                case SearcherFlag.CONSULT:
                    FormDetailDesigner(data, title=f"Consultar Datos de {current_model.nombre_completo}",
                                       is_readonly=True).show()

                case SearcherFlag.DELETE:
                    FormDetailDesigner(
                        data, title=f"Eliminar Datos de {current_model.nombre_completo}", delete_callback=args[1], is_readonly=True).show()

        search = ExamenFisicoPorSistemas()
        search.id = current_model.id
        query, params = to_select_query(search, limit_end=1)
        execute_select(ExamenFisicoPorSistemas, query, show_data, params)
        if foud == False:
            ui.message.show(
                "Error",
                f"Datos no Encontrados de \"{current_model.nombre_completo}\"",
                ui.message.MessageBoxButtons.OK,
                None
            )

class DbEventExamenFisico(object):
    @staticmethod
    def ui_insert(orig: InformacionGeneralPaciente, old: ExamenFisico, new: ExamenFisico):
        try:
            new.id = orig.id
            execute(to_insert_sql(new))
            godjob()
        except Exception as e:
            error(e)
        pass

    @staticmethod
    def ui_custom_show(current_model: InformacionGeneralPaciente, title: str, args: tuple[SearcherFlag, ActionDesigner]):
        foud = False

        def show_data(data):
            nonlocal foud
            foud = True
            match args[0]:
                case SearcherFlag.UPDATE:
                    FormDetailDesigner(data, title=f"Actualizar Datos de {current_model.nombre_completo}",
                                       update_callback=args[1]).show()

                case SearcherFlag.CONSULT:
                    FormDetailDesigner(data, title=f"Consultar Datos de {current_model.nombre_completo}",
                                       is_readonly=True).show()

                case SearcherFlag.DELETE:
                    FormDetailDesigner(
                        data, title=f"Eliminar Datos de {current_model.nombre_completo}", delete_callback=args[1], is_readonly=True).show()

        search = ExamenFisico()
        search.id = current_model.id
        query, params = to_select_query(search, limit_end=1)
        execute_select(ExamenFisico, query, show_data, params)
        if foud == False:
            ui.message.show(
                "Error",
                f"Datos no Encontrados de \"{current_model.nombre_completo}\"",
                ui.message.MessageBoxButtons.OK,
                None
            )


 


class DbSeguimiento(object):
    @staticmethod
    def ui_insert(orig: InformacionGeneralPaciente, old: Seguimiento, new: Seguimiento):
        try:
            new.id = orig.id
            execute(to_insert_sql(new))
            godjob()
        except Exception as e:
            error(e)
        pass
    @staticmethod
    def ui_custom_show_selection(current_model:Any, title: str, args: tuple[SearcherFlag, ActionDesigner]):
        match args[0]:
                case SearcherFlag.UPDATE:
                    FormDetailDesigner(current_model, title=f"Actualizar Datos",
                                        update_callback=args[1]).show()

                case SearcherFlag.CONSULT:
                    FormDetailDesigner(current_model, title=f"Consultar Datos",
                                        is_readonly=True).show()

                case SearcherFlag.DELETE:
                    FormDetailDesigner(
                        current_model, title=f"Eliminar Datos", delete_callback=args[1], is_readonly=True).show()
    pass
    @staticmethod
    def ui_custom_show(current_model: InformacionGeneralPaciente, title: str, args: tuple[SearcherFlag, ActionDesigner]):
        global __ui_custom_show_selection
        foud = False
        table= FormTableShow(title,Seguimiento(),args, custom_show=DbSeguimiento.ui_custom_show_selection)
        def show_data(data):
            nonlocal foud
            foud = True
            table.add_row(data)

            

        search = Seguimiento()
        search.id = current_model.id
        query, params = to_select_query(search)
        execute_select(Seguimiento, query, show_data, params)
        if foud == False:
            ui.message.show(
                "Error",
                f"Datos no Encontrados de \"{current_model.nombre_completo}\"",
                ui.message.MessageBoxButtons.OK,
                None
            )
            table.close()
        else:
            table.show()

class DbEventPlanManejo(object):
    @staticmethod
    def ui_insert(orig: InformacionGeneralPaciente, old: PlanManejo, new: PlanManejo):
        try:
            new.id = orig.id
            execute(to_insert_sql(new))
            godjob()
        except Exception as e:
            error(e)
        pass

    @staticmethod
    def ui_custom_show_selection(current_model:Any, title: str, args: tuple[SearcherFlag, ActionDesigner]):
        match args[0]:
                case SearcherFlag.UPDATE:
                    FormDetailDesigner(current_model, title=f"Actualizar Datos",
                                        update_callback=args[1]).show()

                case SearcherFlag.CONSULT:
                    FormDetailDesigner(current_model, title=f"Consultar Datos",
                                        is_readonly=True).show()

                case SearcherFlag.DELETE:
                    FormDetailDesigner(
                        current_model, title=f"Eliminar Datos", delete_callback=args[1], is_readonly=True).show()
                    
    @staticmethod
    def ui_custom_show(current_model: InformacionGeneralPaciente, title: str, args: tuple[SearcherFlag, ActionDesigner]):
        
        foud = False
        table= FormTableShow(title,PlanManejo(),args, custom_show=DbEventPlanManejo.ui_custom_show_selection)
        def show_data(data):
            nonlocal foud
            foud = True
            table.add_row(data)

            

        search = PlanManejo()
        search.id = current_model.id
        query, params = to_select_query(search)
        execute_select(PlanManejo, query, show_data, params)
        if foud == False:
            ui.message.show(
                "Error",
                f"Datos no Encontrados de \"{current_model.nombre_completo}\"",
                ui.message.MessageBoxButtons.OK,
                None
            )
            table.close()
        else:
            table.show()
class DbEventProfesional(object):
    @staticmethod
    def ui_custom_show_selection(current_model:Any, title: str, args: tuple[SearcherFlag, ActionDesigner]):
        match args[0]:
                case SearcherFlag.UPDATE:
                    FormDetailDesigner(current_model, title=f"Actualizar Datos",
                                        update_callback=args[1]).show()

                case SearcherFlag.CONSULT:
                    FormDetailDesigner(current_model, title=f"Consultar Datos",
                                        is_readonly=True).show()

                case SearcherFlag.DELETE:
                    FormDetailDesigner(
                        current_model, title=f"Eliminar Datos", delete_callback=args[1], is_readonly=True).show()
    @staticmethod
    def ui_insert(orig: InformacionGeneralPaciente, old: Profesional, new: Profesional):
        try:
            new.id = orig.id
            execute(to_insert_sql(new))
            godjob()
        except Exception as e:
            error(e)
        pass

    @staticmethod
    def ui_custom_show(current_model: InformacionGeneralPaciente, title: str, args: tuple[SearcherFlag, ActionDesigner]):
        global __ui_custom_show_selection
        foud = False
        table= FormTableShow(title,Profesional(),args, custom_show=DbEventProfesional.ui_custom_show_selection)
        def show_data(data):
            nonlocal foud
            foud = True
            table.add_row(data)

            

        search = Profesional()
        search.id = current_model.id
        query, params = to_select_query(search)
        execute_select(Profesional, query, show_data, params)
        if foud == False:
            ui.message.show(
                "Error",
                f"Datos no Encontrados de \"{current_model.nombre_completo}\"",
                ui.message.MessageBoxButtons.OK,
                None
            )
            table.close()
        else:
            table.show()