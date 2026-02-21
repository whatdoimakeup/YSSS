from tortoise import Model, fields


class Счетчик(Model):
    id = fields.IntField(primary_key=True)
    chat_id = fields.BigIntField(db_index=True)
    bucket = fields.CharField(max_length=128)
    is_active = fields.BooleanField(default=True, db_index=True)
    created = fields.DatetimeField(auto_now_add=True)
    updated = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "counters"
