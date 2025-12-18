import uuid

class Injector:
    def __init__(self):
        self.registry = {}
        self.singletons = {}
        self.scoped_instances = {}
        self.current_scope = None

    def register(self, interface, provider, lifestyle="PerRequest", params=None):
        self.registry[interface] = {
            "provider": provider,
            "lifestyle": lifestyle,
            "params": params or {}
        }

    def get_instance(self, interface):
        config = self.registry.get(interface)
        if not config:
            raise Exception(f"Интерфейс {interface} не зарегистрирован")

        lifestyle = config["lifestyle"]
        provider = config["provider"]
        params = config["params"]

        if lifestyle == "Singleton":
            if interface not in self.singletons:
                self.singletons[interface] = self.create(provider, params)
            return self.singletons[interface]

        if lifestyle == "Scoped":
            if self.current_scope is None:
                raise Exception("Scope не открыт")
            if interface not in self.scoped_instances:
                self.scoped_instances[interface] = self.create(provider, params)
            return self.scoped_instances[interface]

        return self.create(provider, params)

    def create(self, provider, params):
        if callable(provider) and not isinstance(provider, type):
            return provider()
        
        actual_params = {}
        for name, value in params.items():
            if value in self.registry:
                actual_params[name] = self.get_instance(value)
            else:
                actual_params[name] = value
        return provider(**actual_params)

    def __enter__(self):
        self.current_scope = uuid.uuid4()
        self.scoped_instances = {}
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.current_scope = None
        self.scoped_instances = {}

class Writer: pass
class Database: pass
class Logger: pass

class ConsoleWriter:
    def write(self, msg): print(f"Консоль: {msg}")

class FileWriter:
    def write(self, msg): print(f"Файл: {msg}")

class DevDatabase:
    def __init__(self, writer): self.writer = writer
    def query(self): self.writer.write("Запрос к Dev DB")

class ProdDatabase:
    def __init__(self, writer): self.writer = writer
    def query(self): self.writer.write("Запрос к Prod DB")

class SimpleLogger:
    def log(self): print("Обычный логгер")

class FastLogger:
    def log(self): print("Быстрый логгер")

inj1 = Injector()
inj1.register("Writer", ConsoleWriter, "Singleton")
inj1.register("Database", DevDatabase, "Scoped", {"writer": "Writer"})
inj1.register("Logger", lambda: FastLogger())

inj2 = Injector()
inj2.register("Writer", FileWriter, "PerRequest")
inj2.register("Database", ProdDatabase, "Singleton", {"writer": "Writer"})
inj2.register("Logger", SimpleLogger, "Singleton")

print("--- Тест Конфигурации 1 (Debug) ---")
with inj1:
    db1 = inj1.get_instance("Database")
    db2 = inj1.get_instance("Database")
    print(f"Это один объект в scope? {db1 is db2}")
    db1.query()
    
    log = inj1.get_instance("Logger")
    log.log()

print("\n--- Тест Конфигурации 2 (Release) ---")
w1 = inj2.get_instance("Writer")
w2 = inj2.get_instance("Writer")
print(f"Это разные объекты (PerRequest)? {w1 is not w2}")

db_prod = inj2.get_instance("Database")
db_prod.query()