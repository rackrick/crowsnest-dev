import asyncio
from configparser import SectionProxy

from ..parameter import Parameter
from .. import logger

class Section:
    section_name = 'section'
    keyword = 'section'
    available_sections = {}
    # Section looks like this:
    # [<keyword> <name>]
    # param1: value1
    # param2: value2
    def __init__(self, name: str) -> None:
        self.name = name
        self.parameters: dict[str, Parameter] = {}

    # Parse config according to the needs of the section
    def parse_config_section(self, config_section: SectionProxy, *args, **kwargs) -> bool:
        success = True
        for parameter, value in config_section.items():
            if parameter not in self.parameters:
                logger.log_warning(f"Parameter '{parameter}' is not supported by {self.keyword}!")
                continue
            value = value.split('#')[0].strip()
            self.parameters[parameter].set_value(value)
        for parameter, value in self.parameters.items():
            if value is None:
                logger.log_error(f"Parameter '{parameter}' not found in section "
                                  "[{self.section_name} {self.name}] but is required!")
                success = False
        return success

    # Execute section specific stuff, e.g. starting cam
    async def execute(self, lock: asyncio.Lock):
        raise NotImplementedError("If you see this, a componenent is implemented wrong!!!")


def load_component(*args, **kwargs):
    raise NotImplementedError("If you see this, something went wrong!!!")