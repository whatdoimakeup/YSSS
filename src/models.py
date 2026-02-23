from tortoise import Model, fields


class Счетчик(Model):
    id = fields.IntField(primary_key=True)
    chat_id = fields.BigIntField(db_index=True)
    bucket = fields.CharField(max_length=128)
    is_active = fields.BooleanField(default=True, db_index=True)
    created = fields.DatetimeField(auto_now_add=True)
    updated = fields.DatetimeField(auto_now=True)
    author = fields.ForeignKeyField("src.User", related_name="counters", null=True)

    class Meta:
        table = "counters"


class User(Model):
    id = fields.BigIntField(primary_key=True)
    first_name = fields.CharField(max_length=256, null=True)
    username = fields.CharField(max_length=256, null=True)

    class Meta:
        table = "users"

    @staticmethod
    async def from_telegram_user(telegram_user) -> "User":
        user, created = await User.get_or_create(
            id=telegram_user.id,
            defaults={
                "first_name": telegram_user.first_name,
                "username": telegram_user.username,
            },
        )
        if not created:
            updated_fields = []
            if user.first_name != telegram_user.first_name:
                user.first_name = telegram_user.first_name
                updated_fields.append("first_name")

            if user.username != telegram_user.username:
                user.username = telegram_user.username
                updated_fields.append("username")

            if updated_fields:
                user = await user.save(update_fields=updated_fields)

        return user

    @property
    def user_mention(self):
        if self.username:
            return f"@{self.username}"
        else:
            return f"<a href='tg://user?id={self.id}'>{self.first_name}</a>"
