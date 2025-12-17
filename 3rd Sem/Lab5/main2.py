import json
import os
from dataclasses import dataclass, field, asdict
from typing import Protocol, TypeVar, Sequence, Generic

@dataclass
class User:
    name: str
    login: str
    password: str = field(repr=False)
    email: str | None = None
    address: str | None = None
    id: int | None = None

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
                result = []
                for idx, item_data in enumerate(data, start=1):
                    obj = self.model_type(**item_data)
                    setattr(obj, 'id', idx)
                    result.append(obj)
                return result
        except (json.JSONDecodeError, TypeError) as e:
            print(f"Error decoding JSON from {self.filename}: {e}")
            return []

    def _save_data(self):
        data_to_save = []
        for item in self._data:
            item_dict = asdict(item)
            if 'id' in item_dict:
                del item_dict['id']
            data_to_save.append(item_dict)

        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(data_to_save, f, indent=4, ensure_ascii=False)
        except (PermissionError, OSError) as e:
            print(f"Error writing to file {self.filename}: {e}")

    def get_all(self) -> Sequence[T]:
        return self._data

    def get_by_id(self, id: int) -> T | None:
        return next((item for item in self._data if getattr(item, 'id') == id), None)

    def get_by_login(self, login: str) -> T | None:
        return next((item for item in self._data if getattr(item, 'login') == login), None)

    def add(self, item: T) -> None:
        if self.get_by_login(getattr(item, 'login')) is not None:
            return
        
        current_ids = [getattr(x, 'id') for x in self._data if getattr(x, 'id') is not None]
        new_id = max(current_ids) + 1 if current_ids else 1
        setattr(item, 'id', new_id)
        
        self._data.append(item)
        self._save_data()

    def update(self, item: T) -> None:
        target_id = getattr(item, 'id')
        idx = next((i for i, x in enumerate(self._data) if getattr(x, 'id') == target_id), -1)
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
                    user_login = data.get("user_login")
                    if user_login:
                        self._current_user = self.repo.get_by_login(user_login)
            except (json.JSONDecodeError, TypeError):
                pass
            except (PermissionError, OSError) as e:
                print(f"Error reading session file: {e}")

    def sign_in(self, user: User) -> None:
        self._current_user = user
        try:
            with open(self.session_file, 'w', encoding='utf-8') as f:
                json.dump({"user_login": user.login}, f)
        except (PermissionError, OSError) as e:
            print(f"Error saving session: {e}")

    def sign_out(self) -> None:
        self._current_user = None
        if os.path.exists(self.session_file):
            try:
                os.remove(self.session_file)
            except OSError as e:
                print(f"Error removing session file: {e}")

    @property
    def is_authorized(self) -> bool:
        return self._current_user is not None

    @property
    def current_user(self) -> User | None:
        return self._current_user

def main():
    user_repo = UserRepository("users_db.json")
    auth_service = AuthService(user_repo)

    print(auth_service.current_user)

    u1 = User(name="Boris", login="bobriks_login", password="123", email="b@test.com")
    u2 = User(name="Anna", login="anna_login", password="321")
    
    user_repo.add(u1)
    user_repo.add(u2)
    
    print([f"{u.id}: {u.name}" for u in user_repo.get_all()])

    if os.path.exists("users_db.json"):
        try:
            with open("users_db.json", "r") as f:
                print(f"File content: {f.read()}")
        except OSError as e:
            print(f"Error reading DB file manually: {e}")

    auth_service.sign_in(u1)
    print(f"Current user: {auth_service.current_user}")

if __name__ == "__main__":
    main()