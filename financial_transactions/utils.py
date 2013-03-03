import csv
import sys
from django.utils import translation
from financial_transactions.models import (
    Transaction,
    TransactionCategoryHint,
)


def import_csv(filepath, transaction_form_cls, account, stdout=None):
    stdout = stdout or sys.stdout

    hints = TransactionCategoryHint.objects.all()

    def category_for_import_notes(import_notes):
        """Return a default category based on the import notes."""
        for hint in hints:
            if hint.import_notes_like in import_notes:
                return hint.category
        return None

    translation.activate(transaction_form_cls.locale)

    imported_count = 0
    total_count = 0
    duplicate_count = 0
    categories_set = 0
    with open(filepath, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=transaction_form_cls.delimiter)
        for row in reader:
            total_count += 1

            form = transaction_form_cls(row, account)
            if form.is_valid():
                existing = Transaction.objects.filter(
                    date=form.cleaned_data['date'],
                    amount=form.cleaned_data['amount'],
                    import_notes=form.cleaned_data['import_notes'])
                # XXX should be existing per account too.
                if existing.exists():
                    transaction = existing.get()
                    duplicate_count += 1
                else:
                    # Saved below as the category is null currently.
                    transaction = form.save(commit=False)
                    imported_count += 1

                if transaction.category is None:
                    category = category_for_import_notes(
                        form.cleaned_data['import_notes'])
                    if category is not None:
                        transaction.category = category
                        categories_set += 1
                    transaction.save()
            else:
                stdout.write(
                    u"Error on row: {0}\n: {1}\n".format(
                        row, form.errors.as_text()))
    stdout.write(
        "Imported {imported_count} of {total_count} rows. "
        "{duplicate_count} duplicates found. {categories_set} "
        "categories set.\n".format(
            imported_count=imported_count, total_count=total_count,
            duplicate_count=duplicate_count,
            categories_set=categories_set))
