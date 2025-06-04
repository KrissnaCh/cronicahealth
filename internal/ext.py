from typing import Union
import dearpygui.dearpygui as dpg
import contextlib

# codigo copiado de AblativeAbsolute escrito el Sep 21, 2024
# referencia: https://github.com/hoffstadt/DearPyGui/discussions/2391

@contextlib.contextmanager  # type: ignore
def align_items(n_cols_left: int, n_cols_right: int) -> int | str: # type: ignore
    """Agrega una tabla para alinear elementos.

    Tenga en cuenta:
    Muchos elementos (por ejemplo, combo, drag_*, input_*, slider_*, listbox, progress_bar) no se mostrarán a menos que se establezca un ancho positivo.

    Argumentos:
        n_cols_left: Alinear n elementos a la izquierda. (n_cols_left)
        n_cols_right: Alinear n elementos a la derecha (n_cols_right)
    """
    if n_cols_left < 0 or n_cols_right < 0:
        raise ValueError("Column amount must be 0 or higher")

    table = dpg.add_table(resizable=False, header_row=False, policy=0)
    for _ in range(n_cols_left - 1):
        dpg.add_table_column(width_stretch=False, width_fixed=True, parent=table)
    dpg.add_table_column(width_stretch=False, width_fixed=False, parent=table)
    for _ in range(n_cols_right):
        dpg.add_table_column(width_stretch=False, width_fixed=True, parent=table)
    
    widget = dpg.add_table_row(parent=table)
    if n_cols_left == 0:
        dpg.add_spacer(parent=widget)

    dpg.push_container_stack(widget)
    try:
        yield widget  # type: ignore
    finally:
        return dpg.pop_container_stack()
    