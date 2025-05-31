from dataclasses import fields, is_dataclass
from datetime import date
from enum import Enum, auto
import dearpygui.dearpygui as dpg
from internal import CONTROL, ITEMS, READONLY, REQUIRED, SEARCHABLE, TITLE, Empty, InputWidgetType


class FormDetailDesigner:
    _counter = 0  # Contador de clase para IDs únicos

    def show(self):
        dpg.show_item(self._window_id)

    def __init__(self, model):

        if not is_dataclass(model):
            raise ValueError("entrada debe ser una instancia de dataclass.")

        # Generar ID único
        self._window_id = f"FormDetailDesigner{FormDetailDesigner._counter}"
        self._group_id = f"FormDetailDesigner{FormDetailDesigner._counter}"
        FormDetailDesigner._counter += 1
        self.model = model
        self.designer_fields = [CONTROL, TITLE,
                                READONLY, REQUIRED, ITEMS, SEARCHABLE]
        self.model_type = type(model)
        self.builder = DesignerBuilder()
        self.__create_ui()

    def mark_required(self, str, required) -> str:
        val = Empty.join(str)
        if required == True:
            return val + " *"
        else:
            return val

    def __create_ui(self):
        with dpg.window(tag=self._window_id, label="Información del Paciente", autosize=True, no_collapse=True):
            for f in fields(self.model):
                if all(key in f.metadata for key in self.designer_fields):
                    match f.metadata[CONTROL]:
                        case InputWidgetType.INPUT_INT:
                            self.builder.add_input_int(self.mark_required(
                                f.metadata[TITLE],  f.metadata[REQUIRED]), getattr(self.model, f.name),  f.metadata[READONLY])
                            pass
                        case InputWidgetType.INPUT_TEXT:
                            self.builder.add_input_text(self.mark_required(
                                f.metadata[TITLE], f.metadata[REQUIRED]), getattr(self.model, f.name), f.metadata[READONLY])
                            pass
                        case InputWidgetType.INPUT_FLOAT:
                            self.builder.add_input_float(self.mark_required(
                                f.metadata[TITLE], f.metadata[REQUIRED]), getattr(self.model, f.name), f.metadata[READONLY])
                            pass
                        case InputWidgetType.DATE_PICKER:
                            self.builder.add_date_picker(self.mark_required(
                                f.metadata[TITLE], f.metadata[REQUIRED]), getattr(self.model, f.name), f.metadata[READONLY])
                        case InputWidgetType.COMBO:
                            self.builder.add_combo(self.mark_required(
                                f.metadata[TITLE], f.metadata[REQUIRED]), f.metadata[ITEMS], getattr(self.model, f.name), f.metadata[READONLY])
                        case _:
                            pass


class DesignerBuilder:
    def add_input_text(self, label, default_value, _readonly) -> (int | str):
        with dpg.group(horizontal=True):
            dpg.add_text(label)
            return dpg.add_input_text(
                default_value=default_value if default_value else "", readonly=_readonly
            )

    def add_input_int(self, label, default_value, _readonly) -> (int | str):
        if _readonly == False:
            with dpg.group(horizontal=True):
                dpg.add_text(label)
                return dpg.add_input_int(
                    default_value=default_value if default_value else 0,
                    min_value=0,
                    min_clamped=True
                )
        else:
            return self.add_input_text(label, str(default_value), _readonly)

    def add_input_float(self, label, default_value, _readonly) -> (int | str):
        if _readonly == False:
            with dpg.group(horizontal=True):
                dpg.add_text(label)
                return dpg.add_input_float(
                    default_value=default_value if default_value else 0,
                    min_value=0,
                    min_clamped=True,
                    readonly=_readonly
                )
        else:
            return self.add_input_text(label, str(default_value), _readonly)

    def add_combo(self, label,  items, default_value, readonly) -> (int | str):
        if readonly == False:
            with dpg.group(horizontal=True):
                dpg.add_text(label)
                return dpg.add_combo(
                    items=items,
                    default_value=default_value if default_value else ""
                )
        else:
            return self.add_input_text(label, default_value, readonly)

    def add_date_picker(self, label, default_date: date, readonly) -> (int | str):
        if readonly == False:
            with dpg.group(horizontal=True):
                dpg.add_text(label)
                if default_date:
                    return dpg.add_date_picker(
                        default_value={
                            'year': default_date.year-1900,
                            'month': default_date.month-1,
                            'month_day': default_date.day
                        }
                    )
                else:
                    return dpg.add_date_picker()
        else:
            return self.add_input_text(label, default_date.strftime("%d/%m/%Y") if default_date else "", readonly)


class FormSearcherDesigner:
    _counter = 0  # Contador de clase para IDs únicos

    def show(self):
        dpg.show_item(self._window_id)

    def __init__(self, model):
        if not is_dataclass(model):
            raise ValueError("entrada debe ser una instancia de dataclass.")

        # Generar ID único
        self._window_id = f"FormSearcherDesigner{FormSearcherDesigner._counter}"
        FormSearcherDesigner._counter += 1
        self.model = model
        self.designer_fields = [CONTROL, TITLE,
                                READONLY, REQUIRED, ITEMS, SEARCHABLE]
        self.model_type = type(model)
        self.builder = DesignerBuilder()
        self.__create_ui()

    def __create_ui(self):
        with dpg.window(tag=self._window_id, label="Buscar Paciente", autosize=True, no_collapse=True):
            for f in fields(self.model):
                if all(key in f.metadata for key in self.designer_fields):
                    if f.metadata[SEARCHABLE] == True:
                        match f.metadata[CONTROL]:
                            case InputWidgetType.INPUT_INT:
                                self.builder.add_input_int(f.metadata[TITLE], getattr(
                                    self.model, f.name),  f.metadata[READONLY])
                                pass
                            case InputWidgetType.INPUT_TEXT:
                                self.builder.add_input_text(f.metadata[TITLE], getattr(
                                    self.model, f.name), f.metadata[READONLY])
                                pass
                            case InputWidgetType.INPUT_FLOAT:
                                self.builder.add_input_float(f.metadata[TITLE], getattr(
                                    self.model, f.name), f.metadata[READONLY])
                                pass
                            case InputWidgetType.DATE_PICKER:
                                self.builder.add_date_picker(f.metadata[TITLE], getattr(
                                    self.model, f.name), f.metadata[READONLY])
                            case InputWidgetType.COMBO:
                                self.builder.add_combo(f.metadata[TITLE], f.metadata[ITEMS], getattr(
                                    self.model, f.name), f.metadata[READONLY])
                            case _:
                                pass
