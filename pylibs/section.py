import re
from configparser import SectionProxy

from .parameter import Parameter
from . import logger

class Section:
    section_name = 'Section'
    keyword = 'Section'
    available_sections = {}
    # Section looks like this:
    # [<keyword> <name>]
    # param1
    # param2
    def __init__(self, name: str = '') -> None:
        self.name = name
        self.parameters: dict[str, Parameter] = {}

    # Parse config according to the needs of the section
    def parse_config(self, config_section: SectionProxy, *args, **kwargs) -> bool:
        success = True
        for parameter in config_section:
            value = config_section[parameter]
            if parameter not in self.parameters:
                print(f"Warning: Parameter {parameter} is not supported by {self.keyword}")
                continue
            value = value.split('#')[0].strip()
            self.parameters[parameter].set_value(value)
        for parameter in self.parameters:
            if self.parameters[parameter].value is None:
                logger.log_error(f"Parameter {parameter} not found in Section [{self.section_name} {self.name}]")
                success = False
        return success

    # Execute section specific stuff, e.g. starting cam
    async def execute(self):
        raise NotImplementedError("If you see this, a module is implemented wrong!!!")