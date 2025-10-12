from dataclasses import dataclass


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
    comp_id: str


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
