from django.contrib import admin
from .models import Klient, TovarGroup, Tovar, Part, Account, ExpenseArticle, Transaction, BalanceSnapshot, ClosedPeriod

@admin.register(Klient)
class KlientAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_self')
    search_fields = ('name',)

@admin.register(TovarGroup)
class TovarGroupAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Tovar)
class TovarAdmin(admin.ModelAdmin):
    list_display = ('name', 'group')
    list_filter = ('group',)
    search_fields = ('name',)

@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = ('tovar', 'date', 'purchase_price', 'initial_qty')
    list_filter = ('tovar', 'date')

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(ExpenseArticle)
class ExpenseArticleAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('date', 'operation_type', 'in_guid', 'out_guid', 'amount', 'quantity')
    list_filter = ('operation_type', 'date')
    search_fields = ('in_guid', 'out_guid', 'comment')

@admin.register(BalanceSnapshot)
class BalanceSnapshotAdmin(admin.ModelAdmin):
    list_display = ('guid', 'date', 'quantity', 'amount')
    list_filter = ('date',)

@admin.register(ClosedPeriod)
class ClosedPeriodAdmin(admin.ModelAdmin):
    list_display = ('year', 'month', 'closed_at', 'closed_by')
