from dataclasses import dataclass

class LoggedAccess:
    def __get__(self, instance, owner):
        value = getattr(instance, self.private_name)
        print(f"Получили доступ к атрибуту {self.public_name} со значением:", value)
        return value

    def __set__(self, instance, value):
        print(f"Установим значение атрибута {self.public_name}:", value)
        setattr(instance, self.private_name, value)

    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = "_" + name

@dataclass
class AlertMessage:
    warehouse_id: int = LoggedAccess()

msg = AlertMessage(42)
print(msg)