import json

class TextBuffer:
    def __init__(self, filename="output.txt"):
        self.text = []
        self.filename = filename
        self.clear_file()

    def clear_file(self):
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                f.write("")
        except IOError as e:
            print(f"Ошибка очистки файла {self.filename}: {e}")

    def update_file(self):
        content = "".join(self.text)
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"TEXT FILE (Файл '{self.filename}' обновлен): {content}")
        except IOError as e:
            print(f"Ошибка записи в файл {self.filename}: {e}")

    def add_char(self, char):
        self.text.append(char)
        self.update_file()

    def remove_last(self):
        if self.text:
            self.text.pop()
        self.update_file()

    def show(self):
        # show теперь интегрирован в update_file
        pass


class BaseCommand:
    def execute(self):
        pass
    def undo(self):
        pass
    def get_data(self):
        pass

class TypeCommand(BaseCommand):
    def __init__(self, buffer, char):
        self.buffer = buffer
        self.char = char

    def execute(self):
        self.buffer.add_char(self.char)

    def undo(self):
        self.buffer.remove_last()
    
    def get_data(self):
        return {"type": "type", "char": self.char}

class VolumeCommand(BaseCommand):
    def __init__(self, direction):
        self.direction = direction

    def execute(self):
        action = "увеличена" if self.direction == "up" else "уменьшена"
        print(f"Громкость {action}")

    def undo(self):
        action = "уменьшена" if self.direction == "up" else "увеличена"
        print(f"Громкость {action} (отмена)")

    def get_data(self):
        return {"type": "volume", "dir": self.direction}

class MediaCommand(BaseCommand):
    def execute(self):
        print("Плеер запущен")

    def undo(self):
        print("Плеер закрыт")

    def get_data(self):
        return {"type": "media"}


class Keyboard:
    def __init__(self, buffer):
        self.keys = {}
        self.history = []
        self.redo_stack = []
        self.buffer = buffer

    def bind(self, key, command):
        self.keys[key] = command

    def press(self, key):
        if key in self.keys:
            cmd = self.keys[key]
            cmd.execute()
            self.history.append(cmd)
            self.redo_stack.clear()
        else:
            print(f"Клавиша '{key}' не настроена")

    def undo(self):
        if self.history:
            print("Отмена")
            cmd = self.history.pop()
            cmd.undo()
            self.redo_stack.append(cmd)

    def redo(self):
        if self.redo_stack:
            print("Повтор")
            cmd = self.redo_stack.pop()
            cmd.execute()
            self.history.append(cmd)

class Serializer:
    @staticmethod
    def to_json(data, filename):
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
        except IOError as e:
            print(f"Ошибка записи: {e}")
            with open("default.json", 'w', encoding='utf-8') as f:
                json.dump({}, f, indent=4)
            print(f"Default создан")
        except json.JSONDecodeError as e:
            print(f"Ошибка JSON: {e}")
        except Exception as e:
            print(f"Ошибка: {e}")

    @staticmethod
    def from_json(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except FileNotFoundError:
            print(f"Файл не найден: {filename}")
            return {}
        except json.JSONDecodeError as e:
            print(f"Ошибка JSON: {e}")
            return {}
        except IOError as e:
            print(f"Ошибка чтения: {e}")
            return {}
        except Exception as e:
            print(f"Ошибка: {e}")
            return {}

class DefaultConfigProvider:
    @staticmethod
    def get_default_config(buffer):
        return {
            "a": TypeCommand(buffer, "a").get_data(),
            "b": TypeCommand(buffer, "b").get_data(),
            "c": TypeCommand(buffer, "c").get_data(),
            "ctrl+up": VolumeCommand("up").get_data(),
            "ctrl+down": VolumeCommand("down").get_data(),
            "ctrl+p": MediaCommand().get_data(),
        }

class DictMapper:
    def __init__(self, buffer):
        self.buffer = buffer

    def command_to_dict(self, command):
        return command.get_data()

    def dict_to_command(self, data):
        c_type = data.get("type")
        if c_type == "type":
            return TypeCommand(self.buffer, data.get("char"))
        elif c_type == "volume":
            return VolumeCommand(data.get("dir"))
        elif c_type == "media":
            return MediaCommand()
        return None

class KeyboardStateSaver:
    def __init__(self, serializer, mapper):
        self.serializer = serializer
        self.mapper = mapper

    def save(self, keyboard, filename):
        data_to_save = {}
        for key, cmd in keyboard.keys.items():
            data_to_save[key] = self.mapper.command_to_dict(cmd)
        
        self.serializer.to_json(data_to_save, filename)

    def load(self, keyboard, filename, buffer=None):
        data = self.serializer.from_json(filename)
        
        if not data and buffer:
            data = DefaultConfigProvider.get_default_config(buffer)
        
        for key, cmd_data in data.items():
            cmd = self.mapper.dict_to_command(cmd_data)
            if cmd:
                keyboard.bind(key, cmd)


if __name__ == "__main__":
    FILE_NAME = "output.txt"
    print(f"Используемый файл для вывода: {FILE_NAME}")
    buf = TextBuffer(FILE_NAME)
    kb = Keyboard(buf)

    kb.bind("a", TypeCommand(buf, "a"))
    kb.bind("b", TypeCommand(buf, "b"))
    kb.bind("c", TypeCommand(buf, "c"))
    kb.bind("ctrl+up", VolumeCommand("up"))
    kb.bind("ctrl+down", VolumeCommand("down"))
    kb.bind("ctrl+p", MediaCommand())
    kb.bind("MEME", TypeCommand(buf, "☆*: .｡. o(≧▽≦)o .｡.:*☆)"))

    print("\n--- Ввод текста ---")
    kb.press("a")
    kb.press("b")
    kb.press("c")
    

    print("\n--- Откат ---")
    kb.undo() 
    kb.undo() 

    print("\n--- Повтор ---")
    kb.redo() 

    print("\n--- Другие команды ---")
    kb.press("ctrl+up")
    kb.press("ctrl+p")
    kb.press("MEME")

    print("\n--- Откат 'MEME' ---")
    kb.undo() 

    mapper = DictMapper(buf)
    saver = KeyboardStateSaver(Serializer(), mapper)
    saver.save(kb, "keyboard_config.json")

    print("\n--- Перезагрузка и новый ввод ---")
    new_kb = Keyboard(buf) 
    saver.load(new_kb, "keyboard_config.json", buf)
    
    new_kb.press("a") 
    new_kb.press("ctrl+p")
