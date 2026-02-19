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

    def получить_счетчик(self, chat_id: int, bucket: str) -> int:
        """Узнаем"""
        return self.данные.get(str(chat_id), {}).get(bucket, 0)

    def получить_все_счетчики(self, chat_id: int) -> dict:
        """Узнаем все счетчики для чата"""
        return self.данные.get(str(chat_id), {})

    def увеличить_счетчик(self, chat_id: int, метрика: str) -> int:
        print(f"Увеличиваем счетчик для чата {chat_id} и метрики {метрика}")
        """Повышаем"""
        айди_чата = str(chat_id)
        if айди_чата not in self.данные:
            self.данные[айди_чата] = {}

        значение_метрики = self.данные[айди_чата].get(метрика, None)
        if значение_метрики is None:
            self.данные[айди_чата][метрика] = 0

        self.данные[айди_чата][метрика] = self.данные[айди_чата].get(метрика, 0) + 1
        self.сохранить()
        return self.данные[айди_чата][метрика]

    def уменьшить_счетчик(self, chat_id: int, метрика: str) -> int:
        print(f"Уменьшаем счетчик для чата {chat_id} и метрики {метрика}")
        """Понижаем"""
        айди_чата = str(chat_id)
        if айди_чата not in self.данные:
            self.данные[айди_чата] = {}

        значение_метрики = self.данные[айди_чата].get(метрика, None)
        if значение_метрики is None:
            self.данные[айди_чата][метрика] = 0

        # Не уменьшаем ниже 0
        if self.данные[айди_чата].get(метрика, 0) > 0:
            self.данные[айди_чата][метрика] -= 1
        self.сохранить()
        return self.данные[айди_чата][метрика]

    def обнулить_счетчик(self, chat_id: int):
        """Обнулиться"""
        айди_чата = str(chat_id)
        self.данные[айди_чата] = {}
        self.сохранить()


# Инициализируем хранилище
хранилище = Хранилище()
