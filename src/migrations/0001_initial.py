from tortoise import migrations
from tortoise.migrations import operations as ops
from tortoise import fields


class Migration(migrations.Migration):
    initial = True

    operations = [
        ops.CreateModel(
            name="Счетчик",
            fields=[
                ("id", fields.IntField(generated=True, primary_key=True, unique=True, db_index=True)),
                ("chat_id", fields.BigIntField(db_index=True)),
                ("bucket", fields.CharField(max_length=128)),
                ("is_active", fields.BooleanField(default=True, db_index=True)),
                ("created", fields.DatetimeField(auto_now=False, auto_now_add=True)),
                ("updated", fields.DatetimeField(auto_now=True, auto_now_add=False)),
            ],
            options={"table": "counters", "app": "src", "pk_attr": "id"},
            bases=["Model"],
        ),
    ]
