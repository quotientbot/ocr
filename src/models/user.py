from tortoise import models, fields
from enum import Enum

__all__ = ("User", "Transaction", "TransactionType")


class TransactionType(Enum):
    debit = "DEBIT"
    credit = "CREDIT"


class User(models.Model):
    class Meta:
        table = "user_data"

    user_id = fields.BigIntField(pk=True, index=True)
    balance = fields.DecimalField(max_digits=10, decimal_places=2, default=0)
    email = fields.CharField(max_length=100)
    transactions: fields.ManyToManyRelation["Transaction"] = fields.ManyToManyField("models.Transaction")


class Transaction(models.Model):
    class Meta:
        table = "user_transactions"

    id = fields.CharField(pk=True, max_length=100)
    amount = fields.DecimalField(max_digits=10, decimal_places=2)
    type = fields.CharEnumField(TransactionType)
    created_at = fields.DatetimeField(auto_now=True)
