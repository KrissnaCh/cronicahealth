import dearpygui.dearpygui as dpg
from datetime import date
from typing import Optional


class PacienteViewModel:
    _counter = 0  # Contador de clase para IDs únicos
    
    def __init__(self, model):
        # Generar ID único
        self._window_id = f"dialog_{PacienteViewModel._counter}"
        self._group_id = f"group_{PacienteViewModel._counter}"
        PacienteViewModel._counter += 1
        self.model = model
        self.ui_elements = {}
        self.setup_ui()

    def setup_ui(self):
        with dpg.window(tag=self._window_id, label="Información del Paciente", width=600, height=800):
            with dpg.group(tag=self._group_id):
                
                with dpg.group(horizontal=True):
                    dpg.add_text("ID:")
                    self.ui_elements["id"] = dpg.add_input_text(
                        default_value=str(self.model.id),
                        enabled=False
                    )

                # Campos requeridos
                self._add_input_text("Nombre Completo*", "nombre_completo", self.model.nombre_completo)
                self._add_date_picker("Fecha de Nacimiento*", "fecha_nacimiento", self.model.fecha_nacimiento)
                self._add_combo("Sexo*", "sexo", ["masculino", "femenino", "otro"], self.model.sexo)
                self._add_input_text("Cédula*", "cedula", self.model.cedula)
                self._add_input_text("Dirección*", "direccion", self.model.direccion)

                # Campos opcionales
                self._add_input_int("Edad", "edad", self.model.edad)
                self._add_input_text("Género", "genero", self.model.genero)
                self._add_input_text("Teléfono", "telefono", self.model.telefono)
                self._add_input_text("Email", "email", self.model.email)
                self._add_combo("Estado Civil", "estado_civil", 
                               ["soltero", "casado", "divorciado", "viudo", "otro"], 
                               self.model.estado_civil)
                self._add_input_text("Ocupación", "ocupacion", self.model.ocupacion)

                # Botones y mensajes
                with dpg.group(horizontal=True):
                    dpg.add_button(label="Guardar", callback=self._save_data)
                    dpg.add_button(label="Limpiar", callback=self._clear_form)
                
                self.ui_elements["error_log"] = dpg.add_text("", color=(255, 0, 0))

    def _add_input_text(self, label, field, default_value):
        with dpg.group(horizontal=True):
            dpg.add_text(label)
            self.ui_elements[field] = dpg.add_input_text(
                default_value=default_value if default_value else ""
            )

    def _add_input_int(self, label, field, default_value):
        with dpg.group(horizontal=True):
            dpg.add_text(label)
            self.ui_elements[field] = dpg.add_input_int(
                default_value=default_value if default_value else 0,
                min_value=0,
                min_clamped=True
            )

    def _add_combo(self, label, field, items, default_value):
        with dpg.group(horizontal=True):
            dpg.add_text(label)
            self.ui_elements[field] = dpg.add_combo(
                items=items,
                default_value=default_value if default_value else ""
            )
    
    def _add_date_picker(self, label, field, default_date):
        with dpg.group(horizontal=True):
            dpg.add_text(label)
            self.ui_elements[field] = dpg.add_date_picker(
                default_value={
                    'year': default_date.year-1900,
                    'month': default_date.month-1,
                    'month_day': default_date.day
                } 
            )

    def _validate_inputs(self):
        errors = []
        required_fields = {
            "nombre_completo": "Nombre completo es requerido",
            "cedula": "Cédula es requerida",
            "direccion": "Dirección es requerida",
            "sexo": "Sexo es requerido"
        }

        for field, message in required_fields.items():
            value = dpg.get_value(self.ui_elements[field])
            if not value.strip():
                errors.append(message)

        # Validación adicional para fecha de nacimiento
        date_value = dpg.get_value(self.ui_elements["fecha_nacimiento"])
        if not date_value or not all(key in date_value for key in ['year', 'month', 'month_day']):
            errors.append("Fecha de nacimiento inválida")

        return errors

    def _save_data(self):
        errors = self._validate_inputs()
        if errors:
            dpg.set_value(self.ui_elements["error_log"], "\n".join(errors))
            return

        try:
            # Actualizar el modelo con los valores de la UI
            date_data = dpg.get_value(self.ui_elements["fecha_nacimiento"])
            self.model.fecha_nacimiento = date(
                date_data["year"],
                date_data["month"],
                date_data["month_day"]
            )

            self.model.nombre_completo = dpg.get_value(self.ui_elements["nombre_completo"]).strip()
            self.model.cedula = dpg.get_value(self.ui_elements["cedula"]).strip()
            self.model.direccion = dpg.get_value(self.ui_elements["direccion"]).strip()
            self.model.sexo = dpg.get_value(self.ui_elements["sexo"]).strip()

            # Campos opcionales
            self.model.edad = dpg.get_value(self.ui_elements["edad"]) or None
            self.model.genero = dpg.get_value(self.ui_elements["genero"]).strip() or None
            self.model.telefono = dpg.get_value(self.ui_elements["telefono"]).strip() or None
            self.model.email = dpg.get_value(self.ui_elements["email"]).strip() or None
            self.model.estado_civil = dpg.get_value(self.ui_elements["estado_civil"]).strip() or None
            self.model.ocupacion = dpg.get_value(self.ui_elements["ocupacion"]).strip() or None

            # Aquí iría la lógica para guardar en base de datos
            dpg.set_value(self.ui_elements["error_log"], "Datos guardados exitosamente!")

        except Exception as e:
            dpg.set_value(self.ui_elements["error_log"], f"Error: {str(e)}")

    def _clear_form(self):
        for field in self.ui_elements.values():
            if dpg.get_item_type(field) == "mvAppItemType::mvInputText":
                dpg.set_value(field, "")
            elif dpg.get_item_type(field) == "mvAppItemType::mvInputInt":
                dpg.set_value(field, 0)
            elif dpg.get_item_type(field) == "mvAppItemType::mvDatePicker":
                today = date.today()
                dpg.set_value(field, {'year': today.year, 'month': today.month, 'month_day': today.day})

    def update_model(self, new_model):
        self.model = new_model
        self._update_ui()

    def _update_ui(self):
        dpg.set_value(self.ui_elements["id"], str(self.model.id))
        dpg.set_value(self.ui_elements["nombre_completo"], self.model.nombre_completo)
        dpg.set_value(self.ui_elements["cedula"], self.model.cedula)
        dpg.set_value(self.ui_elements["direccion"], self.model.direccion)
        dpg.set_value(self.ui_elements["sexo"], self.model.sexo)
        
        if self.model.fecha_nacimiento:
            dpg.set_value(self.ui_elements["fecha_nacimiento"], {
                'year': self.model.fecha_nacimiento.year,
                'month': self.model.fecha_nacimiento.month,
                'month_day': self.model.fecha_nacimiento.day
            })

        # Campos opcionales
        for field in ["edad", "genero", "telefono", "email", "estado_civil", "ocupacion"]:
            value = getattr(self.model, field)
            if value is not None:
                dpg.set_value(self.ui_elements[field], value)