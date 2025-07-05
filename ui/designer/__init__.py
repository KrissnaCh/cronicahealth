from enum import Enum, auto
import dearpygui.dearpygui as dpg

window_count = 0
window_base_x = 10  # posición X fija
window_base_y = 50  # posición Y inicial
window_spacing = 15  # distancia vertical entre ventanas


def regtexture(path, tag):
    width, height, channels, data = dpg.load_image(path)
    with dpg.texture_registry():
        dpg.add_static_texture(width, height, data, tag=tag)


class SearcherFlag(Enum):
    INSERT = auto()
    UPDATE = auto()
    DELETE = auto()
    CONSULT = auto()