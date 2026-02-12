import json
import os

БАЗА_ДАННЫХ = os.getenv("DB_PATH", "counters.json")


class Хранилище:
    """Простое хранилище для счетчиков на основе JSON"""

    def __init__(self, путь_к_файлу: str = БАЗА_ДАННЫХ):
        self.путь_к_файлу = путь_к_файлу
        self.Загрузить()

    def Загрузить(self):
        """Сюда"""
        if os.path.exists(self.путь_к_файлу):
            with open(self.путь_к_файлу, "r", encoding="utf-8") as f:
                self.данные = json.load(f)
        else:
            self.данные = {}

    def сохранить(self):
        """Туда"""
        with open(self.путь_к_файлу, "w", encoding="utf-8") as f:
            json.dump(self.данные, f, ensure_ascii=False, indent=2)

    def получить_счетчик(self, chat_id: int) -> int:
        """Узнаем"""
        return self.данные.get(str(chat_id), 0)

    def увеличить_счетчик(self, chat_id: int) -> int:
        """Повышаем"""
        key = str(chat_id)
        self.данные[key] = self.данные.get(key, 0) + 1
        self.сохранить()
        return self.данные[key]

    def обнулить_счетчик(self, chat_id: int):
        """Обнулиться"""
        key = str(chat_id)
        self.данные[key] = 0
        self.сохранить()


# Инициализируем хранилище
хранилище = Хранилище()
