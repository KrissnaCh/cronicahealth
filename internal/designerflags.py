from enum import Enum, auto


class InputWidgetType(Enum):
    INPUT_TEXT = auto()
    INPUT_INT = auto()
    INPUT_FLOAT = auto()
    COMBO = auto()
    DATE_PICKER = auto()

class DesignerField():
    def __init__(self, tcontrol:InputWidgetType, title:str, readonly= False, required = True, items =[]):
        self.tcontrol = tcontrol
        self.title:tuple[str]= title,
        self.readonly= readonly
        self.required = required
        self.items = items