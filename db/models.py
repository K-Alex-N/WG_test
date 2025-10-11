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
class Weapon:
    comp_id: str
    reload_speed: int
    rotational_speed: int
    diameter: int
    power_volley: int
    count: int


@dataclass
class Hull:
    comp_id: str
    armor: int
    type: int
    capacity: int


@dataclass
class Engine:
    comp_id: str
    power: int
    type: int
