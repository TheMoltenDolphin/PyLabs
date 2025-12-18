import uuid

class Injector:
    def __init__(self):
        self.map = {}
        self.singletons = {}
        self.scope_data = {}
        self.is_scope_active = False

    def register(self, interface, target, life_circle="PerRequest", params=None):
        self.map[interface] = {
            "target": target,
            "style": life_circle,
            "params": params or {}
        }

    def get_instance(self, interface):
        if interface not in self.map:
            raise ValueError(f"Ошибка: Интерфейс '{interface}' не зарегистрирован.")

        info = self.map[interface]
        style = info["style"]
        target = info["target"]
        params = info["params"]

        if style == "Singleton":
            if interface not in self.singletons:
                self.singletons[interface] = self.create_object(target, params)
            return self.singletons[interface]

        if style == "Scoped":
            if not self.is_scope_active:
                raise RuntimeError(f"Ошибка: Интерфейс '{interface}' (Scoped) вызван вне блока with.")
            if interface not in self.scope_data:
                self.scope_data[interface] = self.create_object(target, params)
            return self.scope_data[interface]

        return self.create_object(target, params)

    def create_object(self, target, params):
        try:
            if callable(target) and not isinstance(target, type):
                return target()

            args = {}
            for key, value in params.items():
                if isinstance(value, str) and value in self.map:
                    args[key] = self.get_instance(value)
                else:
                    args[key] = value
            
            return target(**args)
        except TypeError as e:
            raise TypeError(f"Ошибка в аргументах конструктора: {e}")

    def __enter__(self):
        self.is_scope_active = True
        self.scope_data = {}
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.is_scope_active = False
        self.scope_data = {}

class Engine: pass
class PetrolEngine: 
    def info(self): return "Бензиновый двигатель"
class ElectricEngine: 
    def info(self): return "Электродвигатель"

class Logger: pass
class DebugLogger:
    def log(self, msg): print(f"[ОТЛАДКА]: {msg}")
class ReleaseLogger:
    def log(self, msg): print(f"[РЕЛИЗ]: {msg}")

class Car: pass
class CityCar:
    def __init__(self, engine, logger):
        self.engine = engine
        self.logger = logger
    def drive(self):
        self.logger.log(f"Запуск. {self.engine.info()}")

inj1 = Injector()
inj1.register("Engine", PetrolEngine, "Singleton")
inj1.register("Logger", DebugLogger, "PerRequest")
inj1.register("Car", CityCar, "Scoped", {"engine": "Engine", "logger": "Logger"})

inj2 = Injector()
inj2.register("Engine", ElectricEngine, "Singleton")
inj2.register("Logger", lambda: ReleaseLogger())
inj2.register("Car", CityCar, "PerRequest", {"engine": "Engine", "logger": "Logger"})

print("--- Тест Конфигурации 1 ---")
with inj1:
    car_a = inj1.get_instance("Car")
    car_b = inj1.get_instance("Car")
    print(f"Объекты совпали в Scope: {car_a is car_b}")
    car_a.drive()

print("\n--- Тест Конфигурации 2 ---")
car_c = inj2.get_instance("Car")
car_d = inj2.get_instance("Car")
print(f"Объекты разные в PerRequest: {car_c is not car_d}")
car_c.drive()

print("\n--- Проверка ошибок ---")
try:
    inj1.get_instance("Car")
except RuntimeError as e:
    print(e)