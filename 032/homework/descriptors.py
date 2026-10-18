from abc import ABC, abstractmethod
from dataclasses import dataclass

class Validator(ABC):
    def __set_name__(self, owner, name):
        self.private_name = "_" + name
        self.name = name


    def __get__(self, instance, owner):
        return getattr(instance, self.private_name)

    def __set__(self, instance, value):
        self.validate(value)
        setattr(instance, self.private_name, value)

    @abstractmethod
    def validate(self, value):
        pass

class OneOf(Validator):
    def __init__(self, *options):
        self.options = set(options)

    def validate(self, value):
        if value not in self.options:
            raise ValueError(f"{self.name}: Ожидается {value!r} среди {self.options!r}")

class Number(Validator):
    def validate(self, value):
        if not isinstance(value, int):
            raise TypeError(f"{self.name}: Ожидается {value!r} числом")
        if value < self.min_value:
            raise ValueError(f"{self.name}: Ожидается значение {value!r} > {self.min_value!r}")
        if value > self.max_value:
            raise ValueError(f"{self.name}: Ожидается значение {value!r} < {self.max_value!r}")

    def __init__(self, min_value, max_value):
        self.min_value = min_value
        self.max_value = max_value

class String(Validator):
    def __init__(self, min_len=None, max_len=None):
        self.min_len = min_len
        self.max_len = max_len

    def validate(self, value):
        if not isinstance(value, str):
            raise TypeError(f"{self.name}: Ожидается {value!r} строкой")
        
        if self.min_len is not None and len(value) < self.min_len:
            raise ValueError(f"{self.name}: Длина строки {len(value)!r} меньше минимальной {self.min_len!r}")
            
        if self.max_len is not None and len(value) > self.max_len:
            raise ValueError(f"{self.name}: Длина строки {len(value)!r} больше максимальной {self.max_len!r}")

class Positive(Validator):
    def validate(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError(f"{self.name}: Ожидается число")

        if value  <= 0:
            raise ValueError(f"{self.name}: Число должно быть больше нуля")

class Typed(Validator):
    def __init__(self, *types):
        self.types = types
        
    def validate(self, value):
        if not isinstance(value, self.types):
            raise TypeError(f"{self.name}: Ожидается {self.types}")
        
@dataclass     
class Component:
    kind:str = OneOf("Металл", "Дерево", "Пластик")
    quantity:int = Number(10,100)
    price:float = Positive()
    name:str = String(min_len = 1, max_len= 10)
    parts:list = Typed(list, str)


    # def __init__(self, kind , quantity, price, name, parts):
    #     self.kind = kind
    #     self.quantity = quantity
    #     self.price = price
    #     self.name = name
    #     self.parts = parts

component = Component("Дерево", 50, 1, "Pavel", "123")
print(component)



# 1. Добавить новый валидатор String
# Пусть принимает параметры min_len и max_len (опциональные). Должен проверять:
#     значение — это str (иначе TypeError);
#     длина в допустимых границах (иначе ValueError).

# 2. Добавить валидатор Positive
# Проверяет, что значение — число (int или float) и больше нуля.

# 3. Валидатор с сообщением об ошибке по имени поля
# Сейчас сообщения не говорят, какое поле не прошло валидацию. Используй __set_name__, чтобы сохранить имя атрибута, и добавь его в текст ошибки. Пример:
# ValueError: quantity: Ожидается значение 9 > 10

# 4. Валидатор Typed
# Принимает ожидаемый тип (или кортеж типов) и проверяет isinstance. Пример использования:
# class User:
#     name = Typed(str)
#     age = Typed(int)