from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Constant(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.JSONField()
    def __str__(self):
        return self.key

class Klient(models.Model):
    name = models.CharField(max_length=200)
    is_self = models.BooleanField(default=False)
    def __str__(self):
        return self.name

class TovarGroup(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Tovar(models.Model):
    name = models.CharField(max_length=200)
    group = models.ForeignKey(TovarGroup, on_delete=models.PROTECT)
    def __str__(self):
        return self.name

class Part(models.Model):
    tovar = models.ForeignKey(Tovar, on_delete=models.CASCADE)
    date = models.DateField()
    purchase_price = models.DecimalField(max_digits=12, decimal_places=2)
    initial_qty = models.DecimalField(max_digits=15, decimal_places=3, validators=[MinValueValidator(0)])
    def __str__(self):
        return f"{self.tovar.name} - {self.date}"

class Account(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class ExpenseArticle(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class OperationType(models.TextChoices):
    PURCHASE = 'purchase', 'Закупка товара'
    SALE_REVENUE = 'sale_rev', 'Выручка от продажи'
    SALE_COST = 'sale_cost', 'Себестоимость продаж'
    PAYMENT_FROM_CLIENT = 'pay_client', 'Оплата от клиента'
    PAYMENT_TO_SUPPLIER = 'pay_supplier', 'Оплата поставщику'
    EXPENSE = 'expense', 'Прочий расход'
    INVENTORY_CORRECTION = 'inventory', 'Корректировка инвентаризации'
    TRANSFER_OWNERSHIP = 'transfer', 'Передача товара (смена владельца)'
    OPENING_BALANCE = 'opening', 'Ввод начальных остатков'

class Transaction(models.Model):
    date = models.DateField(db_index=True)
    operation_type = models.CharField(max_length=20, choices=OperationType.choices, db_index=True)
    in_guid = models.CharField(max_length=255, db_index=True)
    out_guid = models.CharField(max_length=255, db_index=True)
    quantity = models.DecimalField(max_digits=15, decimal_places=3, default=0)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    comment = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    group_uuid = models.UUIDField(null=True, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class BalanceSnapshot(models.Model):
    guid = models.CharField(max_length=255, db_index=True)
    date = models.DateField()
    quantity = models.DecimalField(max_digits=15, decimal_places=3, default=0)
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    class Meta:
        unique_together = [('guid', 'date')]

class ClosedPeriod(models.Model):
    year = models.IntegerField()
    month = models.IntegerField()
    closed_at = models.DateTimeField(auto_now_add=True)
    closed_by = models.ForeignKey(User, on_delete=models.PROTECT)
    class Meta:
        unique_together = [('year', 'month')]
