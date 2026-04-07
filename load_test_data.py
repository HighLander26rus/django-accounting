import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from inventory.models import Klient, Tovar, TovarGroup, Part, Account, ExpenseArticle
from decimal import Decimal

def load():
    self_klient, _ = Klient.objects.get_or_create(name="Я (владелец)", defaults={'is_self': True})
    supplier, _ = Klient.objects.get_or_create(name="Поставщик 1", defaults={'is_self': False})
    buyer, _ = Klient.objects.get_or_create(name="Покупатель 1", defaults={'is_self': False})
    print(f"Клиенты: {self_klient.name}, {supplier.name}, {buyer.name}")

    group, _ = TovarGroup.objects.get_or_create(name="Группа 1")
    print(f"Группа товаров: {group.name}")

    tovar_a, _ = Tovar.objects.get_or_create(name="Товар А", defaults={'group': group})
    tovar_b, _ = Tovar.objects.get_or_create(name="Товар Б", defaults={'group': group})
    print(f"Товары: {tovar_a.name}, {tovar_b.name}")

    part_a, _ = Part.objects.get_or_create(
        tovar=tovar_a, date="2020-01-01",
        defaults={'purchase_price': Decimal('100.00'), 'initial_qty': Decimal('10')}
    )
    part_b, _ = Part.objects.get_or_create(
        tovar=tovar_b, date="2020-01-05",
        defaults={'purchase_price': Decimal('200.00'), 'initial_qty': Decimal('5')}
    )
    print(f"Партии: {part_a}, {part_b}")

    cash, _ = Account.objects.get_or_create(name="Касса")
    bank, _ = Account.objects.get_or_create(name="Расчётный счёт")
    print(f"Счета: {cash.name}, {bank.name}")

    rent, _ = ExpenseArticle.objects.get_or_create(name="Аренда")
    advert, _ = ExpenseArticle.objects.get_or_create(name="Реклама")
    salary, _ = ExpenseArticle.objects.get_or_create(name="Зарплата")
    print(f"Статьи расходов: {rent.name}, {advert.name}, {salary.name}")

    print("\nТестовые данные успешно загружены!")

if __name__ == '__main__':
    load()
