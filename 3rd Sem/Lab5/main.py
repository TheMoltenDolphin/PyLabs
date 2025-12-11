import json
import os
from dataclasses import dataclass, field, asdict
from typing import Protocol, TypeVar, Sequence, Generic, Optional

@dataclass
class User:
    id: int
    name: str
    login: str
    password: str = field(repr=False)
    email: str | None = None
    address: str | None = None

    def __lt__(self, other):
        return self.name < other.name

T = TypeVar('T')

class IDataRepository(Protocol[T]):
    def get_all(self) -> Sequence[T]: ...
    def get_by_id(self, id: int) -> T | None: ...
    def add(self, item: T) -> None: ...
    def update(self, item: T) -> None: ...
    def delete(self, item: T) -> None: ...

class IUserRepository(IDataRepository[User], Protocol):
    def get_by_login(self, login: str) -> User | None: ...

class IAuthService(Protocol):
    def sign_in(self, user: User) -> None: ...
    def sign_out(self) -> None: ...
    
    @property
    def is_authorized(self) -> bool: ...
    
    @property
    def current_user(self) -> User | None: ...


class JsonFileRepository(Generic[T]):
    
    def __init__(self, filename: str, model_type: type):
        self.filename = filename
        self.model_type = model_type
        self._data: list[T] = self._load_data()

    def _load_data(self) -> list[T]:
        if not os.path.exists(self.filename):
            return []
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [self.model_type(**item) for item in data]
        except (json.JSONDecodeError, TypeError) as e:
            repr(f"Ошибка чтения JSON из файла {self.filename}: {e}")
            return []

    def _save_data(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump([asdict(item) for item in self._data], f, indent=4, ensure_ascii=False)

    def get_all(self) -> Sequence[T]:
        return self._data

    def get_by_id(self, id: int) -> T | None:
        return next((item for item in self._data if getattr(item, 'id') == id), None)

    def get_by_login(self, login: int) -> T | None:
        return next((item for item in self._data if getattr(item, 'login') == login), None)

    def add(self, item: T) -> None:
        if self.get_by_login(getattr(item, 'login')) is not None:
            return
        self._data.append(item)
        self._save_data()

    def update(self, item: T) -> None:
        idx = next((i for i, x in enumerate(self._data) if getattr(x, 'id') == getattr(item, 'id')), -1)
        if idx != -1:
            self._data[idx] = item
            self._save_data()

    def delete(self, item: T) -> None:
        self._data = [x for x in self._data if getattr(x, 'id') != getattr(item, 'id')]
        self._save_data()

class UserRepository(JsonFileRepository[User], IUserRepository):
    def __init__(self, filename: str):
        super().__init__(filename, User)

    def get_by_login(self, login: str) -> User | None:
        return next((u for u in self._data if u.login == login), None)

class AuthService(IAuthService):
    def __init__(self, user_repo: IUserRepository, session_file: str = "session.json"):
        self.repo = user_repo
        self.session_file = session_file
        self._current_user: User | None = None
        self._try_auto_auth()

    def _try_auto_auth(self):
        if os.path.exists(self.session_file):
            try:
                with open(self.session_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    user_id = data.get("user_id")
                    if user_id is not None:
                        self._current_user = self.repo.get_by_id(user_id)
            except (json.JSONDecodeError, TypeError) as e:
                print(f"Ошибка чтения JSON из файла {self.session_file}: {e}")

    def sign_in(self, user: User) -> None:
        self._current_user = user
        with open(self.session_file, 'w') as f:
            json.dump({"user_id": user.id}, f)

    def sign_out(self) -> None:
        self._current_user = None
        if os.path.exists(self.session_file):
            os.remove(self.session_file)

    @property
    def is_authorized(self) -> bool:
        return self._current_user is not None

    @property
    def current_user(self) -> User | None:
        return self._current_user


def clean_up_files():
    for f in ["users_db.json", "session.json"]:
        if os.path.exists(f): os.remove(f)

def main():
    print("--- ЗАПУСК 1: Инициализация и создание пользователей ---")

    #clean_up_files()

    user_repo = UserRepository("users_db.json")
    auth_service = AuthService(user_repo)

    u1 = User(id=1, name="Boris", login="boris_login", password="123", email="b@test.com")
    u1 = User(id=4, name="SASHA", login="boris_login", password="123", email="b@test.com")
    u2 = User(id=2, name="Anna", login="anna_login", password="321")
    u3 = User(id=3, name="Clara", login="clara_login", password="abc", address="123 Main St")
    
    user_repo.add(u1)
    user_repo.add(u2)
    user_repo.add(u3)
    print(f"Пользователи добавлены: {[u.name for u in user_repo.get_all()]}")

    sorted_users = sorted(user_repo.get_all())
    print(f"Отсортированный список: {[u.name for u in sorted_users]}")

    u1.email = "new_email@test.com"
    user_repo.update(u1)
    print(f"Email Бориса обновлен: {user_repo.get_by_id(1)}")

    print(f"\nАвторизован ли кто-то? {auth_service.is_authorized}")
    if(auth_service.is_authorized):
        print(f"Текущий пользователь: {auth_service.current_user}")
    auth_service.sign_in(u2)
    print(f"Вход выполнен. Текущий пользователь: {auth_service.current_user}")
    
    auth_service.sign_out()
    auth_service.sign_in(u3)
    print(f"Смена пользователя. Текущий пользователь: {auth_service.current_user}")

    print("\n--- ЗАВЕРШЕНИЕ ПРОГРАММЫ ---")

if __name__ == "__main__":
    main()