# Inspirado en System.Windows.Forms en .NET.

from typing import Callable, Optional
from enum import Enum, auto
import dearpygui.dearpygui as dpg

from internal.ext import align_items


class MessageBoxButtons(Enum):
    """
    Especifica las constantes que definen qué botones se han de mostrar en un MessageBox.
    """

    ABORT_RETRY_IGNORE = auto()
    """El cuadro de mensaje contiene los botones Anular, Reintentar y Omitir."""

    CANCEL_TRY_CONTINUE = auto()
    """Especifica que el cuadro de mensaje contiene los botones Cancelar, Intentar de nuevo y Continuar."""

    OK = auto()
    """El cuadro de mensaje contiene un botón Aceptar."""

    OK_CANCEL = auto()
    """El cuadro de mensaje contiene un botón Aceptar y otro Cancelar."""

    RETRY_CANCEL = auto()
    """El cuadro de mensaje contiene un botón Reintentar y otro Cancelar."""

    YES_NO = auto()
    """El cuadro de mensaje contiene un botón Sí y otro No."""

    YES_NO_CANCEL = auto()
    """El cuadro de mensaje contiene los botones Sí, No y Cancelar."""


class DialogResult(Enum):
    """
    Representa los posibles resultados de un cuadro de diálogo modal.
    Corresponde a los valores devueltos cuando el usuario cierra el diálogo.
    """

    NONE = auto()
    """
    No se devuelve ningún valor del cuadro de diálogo. 
    Esto significa que el diálogo modal continúa ejecutándose.
    """

    OK = auto()
    """
    El valor de retorno del cuadro de diálogo es OK.
    Normalmente enviado desde un botón etiquetado como "Aceptar".
    """

    CANCEL = auto()
    """
    El valor de retorno del cuadro de diálogo es Cancelar.
    Normalmente enviado desde un botón etiquetado como "Cancelar".
    """

    ABORT = auto()
    """
    El valor de retorno del cuadro de diálogo es Abortar.
    Normalmente enviado desde un botón etiquetado como "Abortar".
    """

    RETRY = auto()
    """
    El valor de retorno del cuadro de diálogo es Reintentar.
    Normalmente enviado desde un botón etiquetado como "Reintentar".
    """

    IGNORE = auto()
    """
    El valor de retorno del cuadro de diálogo es Ignorar.
    Normalmente enviado desde un botón etiquetado como "Ignorar".
    """

    YES = auto()
    """
    El valor de retorno del cuadro de diálogo es Sí.
    Normalmente enviado desde un botón etiquetado como "Sí".
    """

    NO = auto()
    """
    El valor de retorno del cuadro de diálogo es No.
    Normalmente enviado desde un botón etiquetado como "No".
    """

    TRY_AGAIN = auto()
    """
    El valor de retorno del cuadro de diálogo es Intentar de nuevo.
    Normalmente enviado desde un botón etiquetado como "Intentar de nuevo".
    """

    CONTINUE = auto()
    """
    El valor de retorno del cuadro de diálogo es Continuar.
    Normalmente enviado desde un botón etiquetado como "Continuar".
    """


class ButtonText:
    """
    Clase que contiene los textos de los botones en español.
    Estos textos se utilizan en los diálogos de mensaje.
    """
    ABORT = "Abortar"
    RETRY = "Reintentar"
    IGNORE = "Ignorar"
    CANCEL = "Cancelar"
    TRY_AGAIN = "Intentar de nuevo"
    CONTINUE = "Continuar"
    OK = "Aceptar"
    YES = "Sí"
    NO = "No"

# Helper function to calculate button width


def __calculate_button_width(labels, padding: int = 20) -> int:
    max_width = 0
    for label in labels:
        text_width, _ = dpg.get_text_size(label)
        if text_width > max_width:
            max_width = text_width
    return int(max_width) + padding


def show(title: str, message: str, buttons: MessageBoxButtons, on_close: Optional[Callable[[DialogResult], None]]):
    """
    Muestra un cuadro de mensaje modal con los botones especificados.

    Args:
        title (str): Título de la ventana del mensaje.
        message (str): Mensaje a mostrar en el cuadro de diálogo.
        buttons (MessageBoxButtons): Enum que especifica los botones a mostrar.
        on_close (callable[[DialogResult], None]): Función que se llamará al cerrar el diálogo, 
            recibiendo como argumento el resultado seleccionado (DialogResult).
    """

    def selection_callback(sender):
        nonlocal on_close
        nonlocal modal_id
        # en caso de que no se haya definido un user_data, se devuelve DialogResult.NONE
        result = dpg.get_item_user_data(sender) or DialogResult.OK
        if on_close:
            on_close(result)
        dpg.delete_item(modal_id)  # Cierra el modal al hacer clic en un botón

     # Determine button labels and widths before creating the window
    match buttons:
        case MessageBoxButtons.ABORT_RETRY_IGNORE:
            labels = [ButtonText.ABORT, ButtonText.RETRY, ButtonText.IGNORE]
        case MessageBoxButtons.CANCEL_TRY_CONTINUE:
            labels = [ButtonText.CANCEL, ButtonText.TRY_AGAIN, ButtonText.CONTINUE]
        case MessageBoxButtons.OK:
            labels = [ButtonText.OK]
        case MessageBoxButtons.OK_CANCEL:
            labels = [ButtonText.OK, ButtonText.CANCEL]
        case MessageBoxButtons.RETRY_CANCEL:
            labels = [ButtonText.RETRY, ButtonText.CANCEL]
        case MessageBoxButtons.YES_NO:
            labels = [ButtonText.YES, ButtonText.NO]
        case MessageBoxButtons.YES_NO_CANCEL:
            labels = [ButtonText.YES, ButtonText.NO, ButtonText.CANCEL]
        case _:
            labels = [ButtonText.OK]

    btn_width = __calculate_button_width(labels)

    # Suponga que el espacio entre los botones es de 8 px (predeterminado en DPG)
    total_buttons_width = btn_width * len(labels) + 8 * (len(labels) - 1) if len(labels) > 1 else btn_width
    
    with dpg.mutex():

        viewport_width = dpg.get_viewport_client_width()
        viewport_height = dpg.get_viewport_client_height()

        with dpg.window(label=title, max_size=(-1,400), modal=True,pos=(viewport_width,viewport_height), no_resize=True, no_close=True) as modal_id:
            
            dpg.add_text(message, wrap=max(total_buttons_width, 400))
            
            dpg.add_separator()
            with align_items(0, 1) :
                with dpg.group(horizontal=True):
                    match buttons:
                        case MessageBoxButtons.ABORT_RETRY_IGNORE:
                            dpg.add_button(label=ButtonText.ABORT, width=btn_width,
                                        user_data=DialogResult.ABORT, callback=selection_callback)
                            dpg.add_button(label=ButtonText.RETRY, width=btn_width,
                                        user_data=DialogResult.RETRY, callback=selection_callback)
                            dpg.add_button(label=ButtonText.IGNORE, width=btn_width,
                                        user_data=DialogResult.IGNORE, callback=selection_callback)

                        case MessageBoxButtons.CANCEL_TRY_CONTINUE:
                            dpg.add_button(label=ButtonText.CANCEL, width=btn_width,
                                        user_data=DialogResult.CANCEL, callback=selection_callback)
                            dpg.add_button(label=ButtonText.TRY_AGAIN, width=btn_width,
                                        user_data=DialogResult.TRY_AGAIN, callback=selection_callback)
                            dpg.add_button(label=ButtonText.CONTINUE, width=btn_width,
                                        user_data=DialogResult.CONTINUE, callback=selection_callback)

                        case MessageBoxButtons.OK:
                            dpg.add_button(label=ButtonText.OK, width=btn_width,
                                        user_data=DialogResult.OK, callback=selection_callback)

                        case MessageBoxButtons.OK_CANCEL:
                            dpg.add_button(label=ButtonText.OK, width=btn_width,
                                        user_data=DialogResult.OK, callback=selection_callback)
                            dpg.add_button(label=ButtonText.CANCEL, width=btn_width,
                                        user_data=DialogResult.CANCEL, callback=selection_callback)

                        case MessageBoxButtons.RETRY_CANCEL:
                            dpg.add_button(label=ButtonText.RETRY, width=btn_width,
                                        user_data=DialogResult.RETRY, callback=selection_callback)
                            dpg.add_button(label=ButtonText.CANCEL, width=btn_width,
                                        user_data=DialogResult.CANCEL, callback=selection_callback)

                        case MessageBoxButtons.YES_NO:
                            dpg.add_button(label=ButtonText.YES, width=btn_width,
                                        user_data=DialogResult.YES, callback=selection_callback)
                            dpg.add_button(label=ButtonText.NO, width=btn_width,
                                        user_data=DialogResult.NO, callback=selection_callback)

                        case MessageBoxButtons.YES_NO_CANCEL:
                            dpg.add_button(label=ButtonText.YES, width=btn_width,
                                        user_data=DialogResult.YES, callback=selection_callback)
                            dpg.add_button(label=ButtonText.NO, width=btn_width,
                                        user_data=DialogResult.NO, callback=selection_callback)
                            dpg.add_button(label=ButtonText.CANCEL, width=btn_width,
                                        user_data=DialogResult.CANCEL, callback=selection_callback)

    # garantizar que estos comandos ocurran en otro marco
    # nota: Posible bug en DPG, 32 es muy rapido y no le da tiempo a calcular el tamaño de la ventana
    # detectado linux fedora 42
    dpg.split_frame()    
    #solucion alternativa, centrar el modal en la pantalla
    width = max(total_buttons_width,400) # dpg.get_item_width(modal_id) or 0
    height = dpg.get_item_height(modal_id) or 0
    dpg.set_item_pos(modal_id, [viewport_width // 2 - width // 2, viewport_height // 2 - height // 2])
    
    

