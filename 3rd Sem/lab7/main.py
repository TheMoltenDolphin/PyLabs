from typing import Callable, Optional, Any, Type, Dict, List, get_type_hints
from enum import Enum
from abc import ABC, abstractmethod

class LifeStyle(Enum):
    PerRequest = "PerRequest"
    Scoped = "Scoped"
    Singleton = "Singleton"

class DIError(Exception):
    pass

class DependencyResolutionError(DIError):
    pass

class RegistrationError(DIError):
    pass

class Injector:
    def __init__(self) -> None:
        self.registered_interfaces: Dict[Any, dict] = {}
        self._scope_stack: List[Dict[Any, Any]] = []
        self._singleton_instances: Dict[Any, Any] = {}

    def register(self, interface: Any, 
                 class_or_factory: Any, 
                 lifestyle: LifeStyle = LifeStyle.PerRequest, 
                 params: Optional[Dict[str, Any]] = None) -> None:
        
        if isinstance(class_or_factory, type):
            target = class_or_factory.__init__
            try:
                hints = get_type_hints(target)
                for name, arg_type in hints.items():
                    if name in ('return', 'self'):
                        continue
                    
                    is_manual = params and name in params
                    
                    if not is_manual and arg_type not in self.registered_interfaces:
                        raise RegistrationError(
                            f"Ошибка регистрации '{class_or_factory.__name__}': "
                            f"параметр '{name}' использует незарегистрированный тип '{arg_type.__name__ if hasattr(arg_type, '__name__') else arg_type}'"
                        )
            except (TypeError, NameError):
                pass

        self.registered_interfaces[interface] = {
            "provider": class_or_factory,
            "lifestyle": lifestyle,
            "params": params if params else {}
        }

    def open_scope(self) -> 'Scope':
        return Scope(self)
    
    def _push_scope(self) -> None:
        self._scope_stack.append({})

    def _pop_scope(self) -> None:
        self._scope_stack.pop()

    def _current_scope(self) -> Optional[Dict]:
        return self._scope_stack[-1] if self._scope_stack else None

    def get_instance(self, interface_type: Any) -> Any:
        if interface_type not in self.registered_interfaces:
            raise DependencyResolutionError(f"Интерфейс {interface_type} не зарегистрирован")

        reg = self.registered_interfaces[interface_type]
        provider = reg["provider"]
        manual_params = reg["params"]
        lifestyle = reg["lifestyle"]

        constructor_args = {}
        target = provider.__init__ if isinstance(provider, type) else provider
        
        try:
            hints = get_type_hints(target)
        except:
            hints = {}

        for name, arg_type in hints.items():
            if name in ('return', 'self'): continue
            
            if name in manual_params:
                constructor_args[name] = manual_params[name]
            elif arg_type in self.registered_interfaces:
                constructor_args[name] = self.get_instance(arg_type)
            else:
                raise DependencyResolutionError(
                    f"Не удалось разрешить зависимость '{name}: {arg_type}'"
                )

        if lifestyle == LifeStyle.PerRequest:
            return provider(**constructor_args)
        
        elif lifestyle == LifeStyle.Singleton:
            if interface_type not in self._singleton_instances:
                self._singleton_instances[interface_type] = provider(**constructor_args)
            return self._singleton_instances[interface_type]
        
        elif lifestyle == LifeStyle.Scoped:
            scope = self._current_scope()
            if scope is None:
                raise RuntimeError("Объект Scoped запрошен вне Scope")
            if interface_type not in scope:
                scope[interface_type] = provider(**constructor_args)
            return scope[interface_type]

class Scope:
    def __init__(self, injector: Injector) -> None:
        self.injector = injector
    def __enter__(self) -> Injector:
        self.injector._push_scope()
        return self.injector
    def __exit__(self, *args) -> None:
        self.injector._pop_scope()

class IBase(ABC):
    @abstractmethod
    def action(self): ...

class IDependency(ABC):
    @abstractmethod
    def work(self): ...

class Dependency(IDependency):
    def work(self): return "работа выполнена"

class Implementation(IBase):
    def __init__(self, dep: IDependency):
        self.dep = dep
    def action(self): return self.dep.work()

class TestClass:
    pass

def run_tests():
    
    inj = Injector()
    try:
        inj.register(IBase, Implementation)
        print("Тест провален: Регистрация с незарегистрированной зависимостью")
    except RegistrationError as e:
        print(f"Тест пройден: Попытка регистрации от незарегистрированного объекта пресечена: {e}")

    inj = Injector()
    inj.register(IDependency, Dependency)
    try:
        inj.register(IBase, Implementation)
        print("Тест пройден: Корректный порядок регистрации (зависимость уже в реестре)")
    except RegistrationError:
        print("Тест провален: Корректный порядок регистрации")

    class Single: pass
    inj.register(Single, Single, lifestyle=LifeStyle.Singleton)
    assert inj.get_instance(Single) is inj.get_instance(Single)
    print("Тест пройден: Singleton возвращает один и тот же экземпляр")

    class ScopedObj: pass
    inj.register(ScopedObj, ScopedObj, lifestyle=LifeStyle.Scoped)
    with inj.open_scope() as s:
        o1 = s.get_instance(ScopedObj)
        o2 = s.get_instance(ScopedObj)
        assert o1 is o2
    print("Тест пройден: Scoped сохраняет объект внутри контекста")

if __name__ == "__main__":
    run_tests()