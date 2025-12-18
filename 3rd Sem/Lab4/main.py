from typing import Any, Protocol, List, Generic, TypeVar

T = TypeVar("T")

class EventHandler(Protocol[T]):
    def handle(self, sender: Any, args: T) -> None: ...

class EventArgs: 
    pass

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

class PropertyChangedEventArgs(EventArgs):
    def __init__(self, prop_name: str):
        self.property_name = prop_name

class PropertyChangingEventArgs(EventArgs):
    def __init__(self, prop_name: str, old_val: Any, new_val: Any):
        self.property_name = prop_name
        self.old_value = old_val
        self.new_value = new_val
        self.can_change = True

class ConsoleLogger(EventHandler[PropertyChangedEventArgs]):
    def handle(self, sender: Any, args: PropertyChangedEventArgs):
        print(f"Консоль: Свойство '{args.property_name}' изменено.")

class FileLogger(EventHandler[PropertyChangedEventArgs]):
    def handle(self, sender: Any, args: PropertyChangedEventArgs):
        filename = "log.txt"
        try:
            with open(filename, "a", encoding="utf-8") as f:
                f.write(f"Файл: {sender} обновил {args.property_name}\n")
        except PermissionError:
            print(f"Ошибка доступа к файлу {filename}")
        except IOError:
            print(f"Ошибка ввода-вывода с файлом {filename}")

class Validator(EventHandler[PropertyChangingEventArgs]):
    def handle(self, sender: Any, args: PropertyChangingEventArgs):
        if args.property_name in ["age", "price"] and (args.new_value < 0):
            print(f"Валидатор: Запрещено отрицательное значение для '{args.property_name}'!")
            args.can_change = False
        if args.property_name == "name" and args.new_value == "":
            print("Валидатор: Имя не может быть пустым!")
            args.can_change = False

class BaseObservable:
    def __init__(self):
        self.on_changed = Event[PropertyChangedEventArgs]()
        self.on_changing = Event[PropertyChangingEventArgs]()

    def _set(self, name: str, current_val: Any, new_val: Any):
        args = PropertyChangingEventArgs(name, current_val, new_val)
        self.on_changing.invoke(self, args)
        
        if not args.can_change:
            return current_val 
        
        self.on_changed.invoke(self, PropertyChangedEventArgs(name))
        return new_val

class Person(BaseObservable):
    def __init__(self, name, age, city):
        super().__init__()
        self._name = name
        self._age = age
        self._city = city

    @property
    def name(self): return self._name
    @name.setter
    def name(self, val): self._name = self._set("name", self._name, val)

    @property
    def age(self): return self._age
    @age.setter
    def age(self, val): self._age = self._set("age", self._age, val)

    @property
    def city(self): return self._city
    @city.setter
    def city(self, val): self._city = self._set("city", self._city, val)

    def __str__(self): return f"Person({self._name}, {self._age})"

class Product(BaseObservable):
    def __init__(self, title, price, stock):
        super().__init__()
        self._title = title
        self._price = price
        self._stock = stock

    @property
    def title(self): return self._title
    @title.setter
    def title(self, val): self._title = self._set("title", self._title, val)

    @property
    def price(self): return self._price
    @price.setter
    def price(self, val): self._price = self._set("price", self._price, val)

    @property
    def stock(self): return self._stock
    @stock.setter
    def stock(self, val): self._stock = self._set("stock", self._stock, val)

    def __str__(self): return f"Product({self._title}, {self._price})"

if __name__ == "__main__":
    p = Person("Ivan", 20, "Omsk")
    prod = Product("Phone", 500, 10)

    console = ConsoleLogger()
    f_log = FileLogger()
    valid = Validator()

    p.on_changing += valid
    p.on_changed += console
    p.on_changed += f_log

    prod.on_changing += valid
    prod.on_changed += console

    print("--- Тест 1: Нормальное изменение ---")
    p.name = "Dmitry"
    prod.price = 600

    print("\n--- Тест 2: Блокировка валидатором ---")
    p.age = -5 
    p.name = ""

    print(f"\nИтог: {p}, Товар стоит: {prod.price}")