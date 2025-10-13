from dataclasses import dataclass, fields

@dataclass
class User:
    name: str
    age: int
    email: str

    def __getitem__(self, item):
        return getattr(self, item)

user = User(name="Алексей", age=30, email="alex@example.com")

# Итерация по атрибутам
for field in fields(user):
    # value = getattr(user, field.name)
    value = field[field.name]
    # print(f"{field.name} = {value}")
    print(field)
    print(value)