"""import database
import dearpygui.dearpygui as dpg

# Variable que almacenará el valor del input
input_value = ""

# Callback que actualiza la variable cuando el input cambia
def input_callback(sender, app_data):
    global input_value
    input_value = app_data  # "app_data" contiene el nuevo valor

if __name__ == "__main__":
    
    def save_callback():
        print("Save Clicked")

    dpg.create_context()
    dpg.create_viewport(vsync=True)
    dpg.setup_dearpygui()

    with dpg.window(label="Example Window"):
        dpg.add_text("Hello world")
        dpg.add_button(label="Save", callback=save_callback)
        dpg.add_input_text(label="string")
        dpg.add_slider_float(label="float")
        dpg.add_input_text(
            label="Texto",
            callback=input_callback,  # Asignar el callback
            tag="input_tag"  # Etiqueta opcional para referencia
        )
        dpg.add_button(
            label="Mostrar Valor",
            callback=lambda: print("Valor actual:", input_value)
        )

    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
    pass"""