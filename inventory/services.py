from decimal import Decimal
from datetime import datetime, date as date_type
from django.db import transaction as db_transaction
from django.utils import timezone
from django.db import models
from .models import Transaction, Part, ClosedPeriod, Constant
from .guid_utils import (
    make_tovar_guid, make_debt_guid, make_cred_guid, make_money_guid
)
from .const import REVENUE_GUID, COST_OF_SALES_GUID

def _to_date(value):
    """Преобразует строку вида 'YYYY-MM-DD' или объект date в date"""
    if isinstance(value, str):
        return datetime.strptime(value, '%Y-%m-%d').date()
    return value

def is_period_closed(date):
    date = _to_date(date)
    return ClosedPeriod.objects.filter(year=date.year, month=date.month).exists()

def get_balance(guid, as_of_date=None):
    if as_of_date:
        as_of_date = _to_date(as_of_date)
    qs = Transaction.objects.filter(in_guid=guid) | Transaction.objects.filter(out_guid=guid)
    if as_of_date:
        qs = qs.filter(date__lte=as_of_date)
    in_sum = qs.filter(in_guid=guid).aggregate(s=models.Sum('amount'))['s'] or Decimal(0)
    out_sum = qs.filter(out_guid=guid).aggregate(s=models.Sum('amount'))['s'] or Decimal(0)
    balance_amount = in_sum - out_sum
    if guid.startswith('tovar_'):
        in_qty = qs.filter(in_guid=guid).aggregate(s=models.Sum('quantity'))['s'] or Decimal(0)
        out_qty = qs.filter(out_guid=guid).aggregate(s=models.Sum('quantity'))['s'] or Decimal(0)
        balance_qty = in_qty - out_qty
        return {'amount': balance_amount, 'quantity': balance_qty}
    return {'amount': balance_amount, 'quantity': None}

def _create_transaction(date, op_type, in_guid, out_guid, amount, quantity=0, comment="", user=None):
    date = _to_date(date)
    if is_period_closed(date):
        raise ValueError(f"Период {date.year}-{date.month:02d} закрыт для изменений.")
    return Transaction.objects.create(
        date=date,
        operation_type=op_type,
        in_guid=in_guid,
        out_guid=out_guid,
        amount=amount,
        quantity=quantity,
        comment=comment,
        user=user
    )

@db_transaction.atomic
def create_purchase(supplier_id, tovar_id, part_id, quantity, purchase_price_per_unit, date=None, user=None):
    if date is None:
        date = timezone.now().date()
    date = _to_date(date)
    amount = Decimal(quantity) * purchase_price_per_unit
    tovar_guid = make_tovar_guid(tovar_id, part_id)
    cred_guid = make_cred_guid(supplier_id)
    _create_transaction(date, 'purchase', tovar_guid, cred_guid, amount, quantity, user=user)

@db_transaction.atomic
def create_sale(client_id, tovar_id, part_id, quantity, sale_price_per_unit, date=None, user=None):
    if date is None:
        date = timezone.now().date()
    date = _to_date(date)
    part = Part.objects.get(id=part_id)
    cost_per_unit = part.purchase_price
    cost_amount = Decimal(quantity) * cost_per_unit
    revenue_amount = Decimal(quantity) * sale_price_per_unit
    tovar_guid = make_tovar_guid(tovar_id, part.id)
    debt_guid = make_debt_guid(client_id)
    _create_transaction(date, 'sale_cost', COST_OF_SALES_GUID, tovar_guid, cost_amount, quantity, user=user)
    _create_transaction(date, 'sale_rev', debt_guid, REVENUE_GUID, revenue_amount, 0, user=user)

@db_transaction.atomic
def create_payment(client_id, amount, money_account_id, date=None, user=None):
    if date is None:
        date = timezone.now().date()
    date = _to_date(date)
    debt_guid = make_debt_guid(client_id)
    money_guid = make_money_guid(money_account_id)
    _create_transaction(date, 'pay_client', money_guid, debt_guid, amount, 0, user=user)
