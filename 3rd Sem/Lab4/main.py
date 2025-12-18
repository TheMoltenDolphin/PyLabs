from typing import Any, Protocol, List, Generic, TypeVar

T = TypeVar("T")

class EventHandler(Protocol[T]):
    def handle(self, sender: Any, args: T) -> None:
        ...

class Event(Generic[T]):
    def __init__(self):
        self._handlers: List[EventHandler[T]] = []

    def __iadd__(self, handler: EventHandler[T]):
        self._handlers.append(handler)
        return self

    def __isub__(self, handler: EventHandler[T]):
        self._handlers.remove(handler)
        return self

    def invoke(self, sender: Any, args: T):
        for handler in self._handlers:
            handler.handle(sender, args)

class PropertyChangedEventArgs:
    def __init__(self, prop_name: str):
        self.property_name = prop_name

class PropertyChangingEventArgs:
    def __init__(self, prop_name: str, old_val: Any, new_val: Any):
        self.property_name = prop_name
        self.old_value = old_val
        self.new_value = new_val
        self.can_change = True

class ConsoleLogger(EventHandler[PropertyChangedEventArgs]):
    def handle(self, sender: Any, args: PropertyChangedEventArgs):
        print(f"Свойство '{args.property_name}' было изменено.")

class FileLogger(EventHandler[PropertyChangedEventArgs]):
    def handle(self, sender: Any, args: PropertyChangedEventArgs):
        filename = "events_log.txt"
        try:
            with open(filename, "a", encoding="utf-8") as f:
                f.write(f"Лог: {sender} изменил {args.property_name}\n")
        except PermissionError:
            print(f"Ошибка: нет прав доступа к файлу {filename}")
        except IOError as e:
            print(f"Ошибка ввода-вывода: {e}")

class Validator(EventHandler[PropertyChangingEventArgs]):
    def handle(self, sender: Any, args: PropertyChangingEventArgs):
        if args.property_name in ["age", "price"] and args.new_value < 0:
            print(f"Внимание: Нельзя установить отрицательное значение для '{args.property_name}'!")
            args.can_change = False

class BaseObservable:
    def __init__(self):
        self.on_changed = Event[PropertyChangedEventArgs]()
        self.on_changing = Event[PropertyChangingEventArgs]()

    def _update(self, name: str, old_val: Any, new_val: Any):
        args_changing = PropertyChangingEventArgs(name, old_val, new_val)
        self.on_changing.invoke(self, args_changing)

        if not args_changing.can_change:
            return old_val 

        self.on_changed.invoke(self, PropertyChangedEventArgs(name))
        return new_val

class Person(BaseObservable):
    def __init__(self, name, age, city):
        super().__init__()
        self._name = name
        self._age = age
        self._city = city

    @property
    def age(self): return self._age
    
    @age.setter
    def age(self, value):
        self._age = self._update("age", self._age, value)
    
    def __str__(self): return f"Человек({self._name}, {self._age})"

class Product(BaseObservable):
    def __init__(self, title, price, stock):
        super().__init__()
        self._title = title
        self._price = price
        self._stock = stock

    @property
    def price(self): return self._price
    
    @price.setter
    def price(self, value):
        self._price = self._update("price", self._price, value)

    def __str__(self): return f"Товар({self._title}, {self._price})"

if __name__ == "__main__":
    user = Person("Алиса", 25, "Москва")
    item = Product("Ноутбук", 1000, 5)

    logger = ConsoleLogger()
    file_log = FileLogger()
    validator = Validator()

    user.on_changing += validator
    item.on_changing += validator

    user.on_changed += logger
    user.on_changed += file_log
    item.on_changed += logger

    print("--- Тест 1: Успешное изменение ---")
    user.age = 26

    print("\n--- Тест 2: Отмена изменения (валидация) ---")
    item.price = -500

    print(f"\nИтог: Возраст: {user.age}, Цена: {item.price}")