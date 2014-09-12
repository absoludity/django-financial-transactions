import sys

from financial_transactions.models import (
    Account,
    Transaction,
    TransactionCategoryHint,
)


def category_for_memo(memo, hints):
    """Return a default category based on the memo."""
    for hint in hints:
        if hint.memo_like in memo:
            return hint.category
    return None


def get_or_create_account(account):
    db_account, created = Account.objects.get_or_create(
        account_id=account.account_id)
    return db_account


def process_transactions_for_account(transactions, account, hints):
    stats = {
        "count": 0,
        "duplicate_count" : 0,
        "imported_count" : 0,
        "categories_set": 0,
    }

    for transaction in transactions:
        stats["count"] += 1

        category = category_for_memo(transaction.memo, hints)

        existing = Transaction.objects.filter(
            tid=transaction.id,
            account=account)
        if existing.exists():
            db_transaction = existing.get()
            stats["duplicate_count"] += 1
            if category != db_transaction.category:
                db_transaction.category = category
                stats["categories_set"] += 1
                db_transaction.save()
        else:
            # Saved below as the category is null currently.
            db_transaction = Transaction.objects.create(
                account=account,
                tid=transaction.id,
                amount=transaction.amount,
                date=transaction.date,
                memo=transaction.memo,
                category=category
            )
            stats["imported_count"] += 1
            if category is not None:
                stats["categories_set"] += 1

    return stats


def import_ofx(ofx, stdout=None):
    stdout = stdout or sys.stdout

    hints = TransactionCategoryHint.objects.all()

    num_accounts = 0
    imported_count = 0
    total_count = 0
    duplicate_count = 0
    categories_set = 0

    for account in ofx.accounts:
        num_accounts += 1
        db_account = get_or_create_account(account)

        transactions = account.statement.transactions
        stats = process_transactions_for_account(transactions, db_account,
                                                 hints)

        imported_count += stats["imported_count"]
        total_count += stats["count"]
        duplicate_count += stats["duplicate_count"]
        categories_set += stats["categories_set"]


    stdout.write(
        "Imported {imported_count} of {total_count} transactions "
        "from {num_accounts} accounts. "
        "{duplicate_count} duplicates found. {categories_set} "
        "categories set.\n".format(
            imported_count=imported_count, total_count=total_count,
            duplicate_count=duplicate_count,
            categories_set=categories_set,
            num_accounts=num_accounts))
