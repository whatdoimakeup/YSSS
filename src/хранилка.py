import os
import sqlite3

БАЗА_ДАННЫХ = os.getenv("DB_PATH", "counters.db")


class Хранилище:
    """Простое хранилище для счетчиков на основе SQLite"""

    def __init__(self, путь_к_файлу: str = БАЗА_ДАННЫХ):
        self.путь_к_файлу = путь_к_файлу
        self._инициализировать_бд()

    def _инициализировать_бд(self):
        """Создаем таблицу если не существует"""
        with sqlite3.connect(self.путь_к_файлу) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS counters (
                    chat_id TEXT NOT NULL,
                    bucket TEXT NOT NULL,
                    value INTEGER NOT NULL DEFAULT 0,
                    PRIMARY KEY (chat_id, bucket)
                )
                """
            )

    def получить_счетчик(self, chat_id: int, bucket: str) -> int:
        """Узнаем"""
        with sqlite3.connect(self.путь_к_файлу) as conn:
            row = conn.execute(
                "SELECT value FROM counters WHERE chat_id = ? AND bucket = ?",
                (str(chat_id), bucket),
            ).fetchone()
        return row[0] if row else 0

    def получить_все_счетчики(self, chat_id: int) -> dict:
        """Узнаем все счетчики для чата"""
        with sqlite3.connect(self.путь_к_файлу) as conn:
            rows = conn.execute(
                "SELECT bucket, value FROM counters WHERE chat_id = ?",
                (str(chat_id),),
            ).fetchall()
        return {bucket: value for bucket, value in rows}

    def увеличить_счетчик(self, chat_id: int, метрика: str) -> int:
        print(f"Увеличиваем счетчик для чата {chat_id} и метрики {метрика}")
        """Повышаем"""
        with sqlite3.connect(self.путь_к_файлу) as conn:
            conn.execute(
                """
                INSERT INTO counters (chat_id, bucket, value) VALUES (?, ?, 1)
                ON CONFLICT(chat_id, bucket) DO UPDATE SET value = value + 1
                """,
                (str(chat_id), метрика),
            )
            row = conn.execute(
                "SELECT value FROM counters WHERE chat_id = ? AND bucket = ?",
                (str(chat_id), метрика),
            ).fetchone()
        return row[0]

    def уменьшить_счетчик(self, chat_id: int, метрика: str) -> int:
        print(f"Уменьшаем счетчик для чата {chat_id} и метрики {метрика}")
        """Понижаем"""
        with sqlite3.connect(self.путь_к_файлу) as conn:
            # Не уменьшаем ниже 0
            conn.execute(
                """
                INSERT INTO counters (chat_id, bucket, value) VALUES (?, ?, 0)
                ON CONFLICT(chat_id, bucket) DO UPDATE SET value = MAX(0, value - 1)
                """,
                (str(chat_id), метрика),
            )
            row = conn.execute(
                "SELECT value FROM counters WHERE chat_id = ? AND bucket = ?",
                (str(chat_id), метрика),
            ).fetchone()
        return row[0]

    def обнулить_счетчик(self, chat_id: int):
        """Обнулиться"""
        with sqlite3.connect(self.путь_к_файлу) as conn:
            conn.execute(
                "DELETE FROM counters WHERE chat_id = ?",
                (str(chat_id),),
            )


# Инициализируем хранилище
хранилище = Хранилище()
