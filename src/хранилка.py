import os
from tortoise.functions import Count

from src.models import User, Счетчик

URL_БАЗЫ_ДАННЫХ = os.getenv("DATABASE_URL", "postgres://ysss:admin@127.0.0.1:5432/ysss")

TORTOISE_ORM = {
    "connections": {"default": URL_БАЗЫ_ДАННЫХ},
    "apps": {
        "src": {
            "models": ["src.models"],
            "default_connection": "default",
            "migrations": "src.migrations",
        }
    },
}


class Хранилище:
    """Хранилище счетчиков на базе PostgreSQL через Tortoise ORM."""

    async def получить_счетчик(self, chat_id: int, bucket: str) -> int:
        """Узнаем значение одного счетчика"""
        return await Счетчик.filter(
            chat_id=chat_id,
            bucket=bucket,
            is_active=True,
        ).count()

    async def получить_все_счетчики(self, chat_id: int) -> dict[str, int]:
        """Узнаем все счетчики для чата"""
        счетчики = (
            await Счетчик.filter(chat_id=chat_id, is_active=True)
            .group_by("bucket")
            .annotate(total=Count("id"))
            .values("bucket", "total")
        )
        return {строка["bucket"]: строка["total"] for строка in счетчики}

    async def добавить_счетчик(self, chat_id: int, author: User, метрика: str) -> Счетчик:
        """Повышаем"""
        print(f"Увеличиваем счетчик для чата {chat_id} и метрики {метрика}")
        новый_счетчик = await Счетчик.create(
            chat_id=chat_id,
            bucket=метрика,
            is_active=True,
            author=author,
        )
        return новый_счетчик

    async def уменьшить_счетчик(self, chat_id: int, id_метрики: int) -> int:
        """Понижаем"""
        print(f"Уменьшаем счетчик для чата {chat_id} и метрики {id_метрики}")
        запись = await Счетчик.filter(
            chat_id=chat_id,
            id=id_метрики,
            is_active=True,
        ).first()

        if запись:
            запись.is_active = False
            await запись.save(update_fields=["is_active"])
        return await self.получить_счетчик(chat_id, запись.bucket if запись else "")


# Инициализируем хранилище
хранилище = Хранилище()
