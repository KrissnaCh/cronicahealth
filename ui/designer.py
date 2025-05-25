from dataclasses import fields, is_dataclass
from datetime import date
from enum import Enum, auto
import dearpygui.dearpygui as dpg
from internal import DesignerP, Empty
from internal.designerflags import DesignerField, InputWidgetType


class Designer:
    _counter = 0  # Contador de clase para IDs únicos

    def show(self):
        dpg.show_item(self._window_id)

    def __add_input_text(self, label, default_value, _readonly) -> (int | str):
        with dpg.group(horizontal=True):
            dpg.add_text(label)
            return dpg.add_input_text(
                default_value=default_value if default_value else "", readonly=_readonly
            )

    def __add_input_int(self, label, default_value, _readonly) -> (int | str):
        if _readonly == False:
            with dpg.group(horizontal=True):
                dpg.add_text(label)
                return dpg.add_input_int(
                    default_value=default_value if default_value else 0,
                    min_value=0,
                    min_clamped=True
                )
        else:
            return self.__add_input_text(label,str(default_value), _readonly)

    def __add_input_float(self, label, default_value, _readonly) -> (int | str):
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
            return self.__add_input_text(label,str(default_value), _readonly)

    def __add_combo(self, label,  items, default_value, readonly) -> (int | str):
        if readonly == False:
            with dpg.group(horizontal=True):
                dpg.add_text(label)
                return dpg.add_combo(
                    items=items,
                    default_value=default_value if default_value else ""
                )
        else:
            return self.__add_input_text(label,default_value, readonly)
        

    def __add_date_picker(self, label, default_date:date, readonly) -> (int | str):
        if readonly == False:
            with dpg.group(horizontal=True):
                dpg.add_text(label)
                if default_date :
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
            return self.__add_input_text(label,default_date.strftime("%d/%m/%Y") if default_date else "", readonly)

    def __init__(self, model):

        if not is_dataclass(model):
            raise ValueError("Input must be a dataclass instance.")

        # Generar ID único
        self._window_id = f"PacienteViewModeldialog_{Designer._counter}"
        self._group_id = f"PacienteViewModelgroup_{Designer._counter}"
        Designer._counter += 1
        self.model = model
        self.model_type = type(model)
        self._create_ui()

    def mark_required(self, str, required) -> str:
        val = Empty.join(str)
        if required == True:
            return val + " *"
        else:
            return val

    def _create_ui(self):
        with dpg.window(tag=self._window_id, label="Información del Paciente", autosize=True,no_collapse=True):
            with dpg.group(tag=self._group_id):

                """with dpg.group(horizontal=True):
                    dpg.add_text("ID:")
                    self.ui_elements["id"] = dpg.add_input_text(
                        default_value=str(self.model.id),
                        enabled=False
                    )"""

                for f in fields(self.model):
                    if f.metadata.__contains__(DesignerP):
                        args: DesignerField = f.metadata[DesignerP]
                        match args.tcontrol:
                            case InputWidgetType.INPUT_INT:
                                self.__add_input_int(self.mark_required(
                                    args.title, args.required), getattr(self.model, f.name), args.readonly)
                                pass
                            case InputWidgetType.INPUT_TEXT:
                                self.__add_input_text(self.mark_required(
                                    args.title, args.required), getattr(self.model, f.name), args.readonly)
                                pass
                            case InputWidgetType.INPUT_FLOAT:
                                self.__add_input_float(self.mark_required(
                                    args.title, args.required), getattr(self.model, f.name), args.readonly)
                                pass
                            case InputWidgetType.DATE_PICKER:
                                self.__add_date_picker(self.mark_required(
                                    args.title, args.required), getattr(self.model, f.name), args.readonly)
                            case InputWidgetType.COMBO:
                                self.__add_combo(self.mark_required(
                                    args.title, args.required),args.items, getattr(self.model, f.name), args.readonly)
                            case _:
                                pass
