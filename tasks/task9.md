# Задание №9: Отчёт «Долги клиентов»
## Цель
Научиться строить отчёты на основе GUID и агрегировать остатки по контрагентам. Использовать `get_balance` для вычисления текущей 
задолженности.
## Исходные данные
- Модели `Klient` и `Transaction` уже созданы. - Функция `get_balance` из `inventory/services.py` умеет возвращать остаток по любому GUID. 
- Долг клиента хранится в транзакциях с GUID вида `debt_{client_id}` (дебетовая задолженность). При продаже создаётся транзакция `sale_rev` 
с `in_guid = debt_{client_id}`, при оплате – `pay_client` с `out_guid = debt_{client_id}`. - В базе есть клиенты с разным состоянием долга.
## Что нужно сделать
Создать страницу для просмотра дебиторской задолженности клиентов. **Страница:** `/reports/client-debts/` **Отчёт должен содержать таблицу 
с колонками:** - Клиент (имя) - Текущий долг (сумма, положительная – клиент должен нам, отрицательная – мы должны клиенту, но для 
дебиторской задолженности обычно показывают только положительные суммы) - Дата последней операции по долгу (опционально) **Фильтры:** - По 
клиенту (выпадающий список) - Показывать только клиентов с ненулевым долгом (чекбокс)
## Технические требования
- Получить всех клиентов (или отфильтрованных) и для каждого вычислить долг через `get_balance(make_debt_guid(client.id))`. - Результат – 
сумма остатка (поле `amount` из возвращаемого словаря). Если долг равен 0, можно не показывать (если выбран соответствующий фильтр). - Для 
даты последней операции можно сделать отдельный запрос: найти максимальную дату транзакций, где `in_guid` или `out_guid` равен 
`debt_{client.id}`. - Выводить итоговую сумму долга по всем отображаемым клиентам.
## Ожидаемый результат
- Таблица клиентов с их текущим долгом. - Фильтр по клиенту работает. - Возможность скрыть клиентов с нулевым долгом. - Итоговая строка с 
общей суммой задолженности.
## Подсказки
- В представлении:
  ```python
  from inventory.guid_utils import make_debt_guid
  from inventory.services import get_balance
  def client_debts(request):
      clients = Klient.objects.filter(is_self=False) # исключаем владельца
      client_id = request.GET.get('client_id')
      hide_zero = request.GET.get('hide_zero') == 'on'
      if client_id:
          clients = clients.filter(id=client_id)
      debts = []
      total_debt = 0
      for client in clients:
          debt_guid = make_debt_guid(client.id)
          balance = get_balance(debt_guid)
          debt_amount = balance['amount']
          if hide_zero and debt_amount == 0:
              continue
          # последняя операция по долгу
          last_op = Transaction.objects.filter(
              in_guid=debt_guid
          ) | Transaction.objects.filter(
              out_guid=debt_guid
          ).order_by('-date').first()
          debts.append({
              'client': client,
              'debt': debt_amount,
              'last_date': last_op.date if last_op else None
          })
          total_debt += debt_amount
      context = {
          'debts': debts,
          'total_debt': total_debt,
          'clients': Klient.objects.filter(is_self=False),
          'selected_client': client_id,
          'hide_zero': hide_zero,
      }
      return render(request, 'inventory/client_debts.html', context)
```
- В шаблоне используйте фильтр `floatformat:2` для отображения сумм.

## Дополнительно (по желанию)

- Добавить возможность показать долги поставщикам (кредиторская задолженность) – отдельный отчёт.
- Экспорт в CSV.

## Критерии приемки

- Отчёт показывает корректные суммы долга для каждого клиента.
- Фильтры работают.
- Итоговая сумма вычислена верно.
- Pull Request из ветки `feature/task9-client-debts`.

## Срок выполнения

1.5 дня.
