from enum import Enum
from typing import Protocol, List
import re
from datetime import date, datetime
import os 


class LogLevel(Enum):
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"
    
class ILogFilter(Protocol):
    def match(self, log_level: LogLevel, text: str) -> bool:
        ...

class ILogHandler(Protocol):
    def handle(self, log_level: LogLevel, text: str) -> None:
        ...

class ILogFormatter(Protocol):
    def format(self, log_level: LogLevel, text: str) -> str:
        ...

class SimpleLogFilter:
    def __init__(self, pattern: str):
        self._pattern = pattern.lower()

    def match(self, log_level: LogLevel, text: str) -> bool:
        return self._pattern in text.lower()

class ReLogFilter:
    def __init__(self, pattern: str):
        try:
            self._compiled_pattern = re.compile(pattern)
        except:
            self._compiled_pattern = re.compile(r'')
            repr("Ошибка в регулярном выражении. Используется выражение по умолчанию")

    def match(self, log_level: LogLevel, text: str) -> bool:
        return bool(self._compiled_pattern.search(text))

class LevelFilter:
    def __init__(self, min_level: LogLevel):
        self._levels_order = {
            LogLevel.INFO: 1,
            LogLevel.WARN: 2,
            LogLevel.ERROR: 3,
        }
        self._min_level_value = self._levels_order[min_level]

    def match(self, log_level: LogLevel, text: str) -> bool:
        return self._levels_order[log_level] >= self._min_level_value

class ConsoleHandler:
    def handle(self, log_level: LogLevel, text: str) -> None:
        print(text)

class FileHandler:
    def __init__(self, filename: str):
        self._filename = filename

    def handle(self, log_level: LogLevel, text: str) -> None:
        try:
            with open(self._filename, 'a', encoding='utf-8') as f:
                f.write(text + '\n')
        except:
            with open("default_logs.txt", 'a', encoding='utf-8') as f:
                f.write(text + '\n')
            repr("Ошибка при чтении/создании файла, создан базовый файл")


class BasicLogFormatter:
    def __init__(self, date_format : str = "%d.%m.%Y %H:%M:%S"):
        self._date_format = date_format

    def format(self, log_level: LogLevel, text: str) -> str:
        timestamp = datetime.now().strftime(self._date_format)
        formatted_text = f"[{log_level.value}] [{timestamp}] {text}"
        return formatted_text
        
class Logger:

    def __init__(
        self,
        filters: List[ILogFilter],
        formatters: List[ILogFormatter],
        handlers: List[ILogHandler]
    ):
        self._filters = filters
        self._formatters = formatters
        self._handlers = handlers
    
    def log(self, log_level: LogLevel, text: str) -> None:
        if not all(f.match(log_level, text) for f in self._filters):
            return

        formatted_text = text
        for formatter in self._formatters:
            formatted_text = formatter.format(log_level, formatted_text, )

        for handler in self._handlers:
            handler.handle(log_level, formatted_text)

    def log_info(self, text: str) -> None:
        self.log(LogLevel.INFO, text)

    def log_warn(self, text: str) -> None:
        self.log(LogLevel.WARN, text)

    def log_error(self, text: str) -> None:
        self.log(LogLevel.ERROR, text)


def demonstrate_logger():
    LOG_FILENAME = "app_logs.txt"
    
    if os.path.exists(LOG_FILENAME):
        os.remove(LOG_FILENAME)
        

    level_filter = LevelFilter(LogLevel.INFO) 
    regex_filter = ReLogFilter(pattern=r'(user|\d{3}|system|\d{4}ms)')

    formatter = BasicLogFormatter("%d-%m-%Y %H-%M-%S хаха тест форматтера")

    console_handler = ConsoleHandler()
    file_handler = FileHandler(LOG_FILENAME)

    my_logger = Logger(
        filters=[level_filter, regex_filter], 
        formatters=[formatter],              
        handlers=[console_handler, file_handler]
    )

    
    my_logger.log_error("Critical system shutdown.")
    
    my_logger.log_info("system configuration loaded.") 

    my_logger.log_warn("Low system memory warning.") 

    my_logger.log_error("Unauthorised user 1001 attempted login.") 

    my_logger.log_warn("Ping of current service is 1000ms.") 

    my_logger.log_warn("API response time 400ms exceeded threshold.") 
    
    my_logger.log_error("It's Fine, HAHA NO!") 

if __name__ == "__main__":
    demonstrate_logger()