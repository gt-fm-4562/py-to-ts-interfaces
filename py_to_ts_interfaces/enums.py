from typing import List
from typing import Type

from py_to_ts_interfaces.constants import ENUM_KIND_INT
from py_to_ts_interfaces.constants import ENUM_KIND_STR, ENUM_KIND_DEFAULT


class EnumElement:
    """Represent one element of an enum."""
    name: str
    value: str
    suffix: str

    def __init__(self, line: str):
        name_and_value = line.strip().split(" = ")
        self.name = name_and_value[0]
        self.value = name_and_value[1].strip("\"")

class EnumStringElement(EnumElement):
    suffix: str = ENUM_KIND_STR

    def get_typescript(self) -> str:
        """Return the element in typescript syntax (including indentation)."""
        return "    {0} = \'{1}\',".format(self.name, self.value)
class EnumDefaultElement(EnumStringElement):
    suffix: str = ENUM_KIND_DEFAULT

class EnumIntegerElement(EnumElement):
    suffix: str = ENUM_KIND_INT

    def get_typescript(self) -> str:
        """Return the element in typescript syntax (including indentation)."""
        return "    {0} = \{1}\,".format(self.name, self.value)



ENUM_KIND_MAP = {ENUM_KIND_STR: EnumStringElement, ENUM_KIND_INT: EnumIntegerElement, ENUM_KIND_DEFAULT: EnumDefaultElement}

class EnumDefinition:
    """Represent a python/typescript enum."""
    name: str
    elements: List[EnumElement]

    def __init__(self, definition: List[str], kind: str = ENUM_KIND_DEFAULT):
        definition = [line for line in definition if
                      not line.startswith("    def") and
                      not line.startswith("        ")
                      ]

        enum_type: Type[EnumDefinition] = ENUM_KIND_MAP[kind]
        suffix: str = enum_type.suffix
        self.name = definition[0].removeprefix("class ").removesuffix(suffix)
        self.elements = [enum_type(line) for line in definition[1:]]

    def get_typescript(self) -> str:
        """Return the enum in typescript syntax (including indentation)."""
        typescript_string = "export enum {0} {{\n".format(self.name)
        for element in self.elements:
            typescript_string += "{}\n".format(element.get_typescript())
        typescript_string += "}"
        return typescript_string
