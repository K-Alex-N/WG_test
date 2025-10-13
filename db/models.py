from dataclasses import dataclass

from config import ENGINES_COUNT, HULLS_COUNT, WEAPONS_COUNT


@dataclass
class Ship:
    ship_id: str
    weapon: str
    hull: str
    engine: str

    def __getitem__(self, item):
        return getattr(self, item)


@dataclass
class Component:
    """parent class for components: weapon, hull, engine"""

    comp_id: str

    def __getitem__(self, item):
        return getattr(self, item)



@dataclass
class Weapon(Component):
    reload_speed: int
    rotational_speed: int
    diameter: int
    power_volley: int
    count: int


@dataclass
class Hull(Component):
    armor: int
    type: int
    capacity: int


@dataclass
class Engine(Component):
    power: int
    type: int


@dataclass
class ComponentStructure:
    """Useful information about components"""

    name: str
    params: list[str]
    table_name: str
    max_component_count: int


# fmt: off
weapon = ComponentStructure(
    "weapon",
    ["reload_speed", "rotational_speed", "diameter", "power_volley", "count"],
    "weapons",
    WEAPONS_COUNT
)

hull = ComponentStructure(
    "hull",
    ["armor", "type", "capacity"],
    "hulls",
    HULLS_COUNT
)

engine = ComponentStructure(
    "engine",
    ["power", "type"],
    "engines",
    ENGINES_COUNT
)
