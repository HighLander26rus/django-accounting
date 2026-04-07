from .const import (
    GUID_PREFIX_DEBT, GUID_PREFIX_CRED, GUID_PREFIX_MONEY, GUID_PREFIX_TOVAR,
    GUID_PREFIX_SKLAD, GUID_PREFIX_EXPENSE
)

def make_debt_guid(klient_id):
    return f"{GUID_PREFIX_DEBT}_{klient_id}"

def make_cred_guid(klient_id):
    return f"{GUID_PREFIX_CRED}_{klient_id}"

def make_money_guid(account_id):
    return f"{GUID_PREFIX_MONEY}_{account_id}"

def make_tovar_guid(tovar_id, part_id):
    return f"{GUID_PREFIX_TOVAR}_{tovar_id}_{part_id}"

def make_sklad_guid(sklad_id, owner_klient_id):
    return f"{GUID_PREFIX_SKLAD}_{sklad_id}_{owner_klient_id}"

def make_expense_guid(article_id):
    return f"{GUID_PREFIX_EXPENSE}_{article_id}"

def parse_guid(guid):
    parts = guid.split('_')
    return {'type': parts[0], 'ids': [int(p) for p in parts[1:]]}
