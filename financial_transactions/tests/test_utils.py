import csv
import datetime
import os
import shutil
import tempfile
from decimal import Decimal
from StringIO import StringIO

from categories.models import Category
from django.core.management import (
    call_command,
    CommandError,
)
from django_factory import TestCase

from financial_transactions.models import (
    Account,
    Transaction,
    TransactionCategoryHint,
)
from financial_transactions.management.commands.import_transactions import (
    Command,
)


def transactions_to_csv_data(transactions):
    for transaction in transactions:
        amount = transaction.amount
        if amount < 0:
            sign = '-'
            amount *= -1
        else:
            sign = '+'
        yield [
            transaction.date.date(),
            transaction.import_notes,
            # XXX There must be a normal way for the decimal
            # to be converted using locale? Use template tag?
            unicode(amount).replace('.', ','),
            sign,
        ]


def write_csv_transactions(transactions, filename):
    with open(filename, 'w+') as csv_file:
        writer = csv.writer(csv_file, delimiter=";")
        for transaction in transactions_to_csv_data(transactions):
            writer.writerow(transaction)


class ImportCSVTransactionsTestCase(TestCase):
    # XXX Move the relevant tests from here to test_utils now
    # that the bulk of the functionality has been refactored
    # there.

    def setUp(self):
        super(ImportCSVTransactionsTestCase, self).setUp()
        self.tmp_dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp_dir)

        self.stdout = StringIO()

    def test_creates_transactions(self):
        self.factory.make_one(Account)
        filename = os.path.join(self.tmp_dir, 'mytrans.csv')
        write_csv_transactions(
            self.factory.prepare(5, Transaction), filename)

        call_command('import_transactions', filename, stdout=self.stdout)

        self.assertEqual(5, Transaction.objects.count())

    def test_transaction_values(self):
        filename = os.path.join(self.tmp_dir, 'mytrans.csv')
        self.factory.make_one(Account)
        write_csv_transactions([
            self.factory.prepare_one(
                Transaction, amount=Decimal('-1234.56'),
                date=datetime.datetime(2013, 2, 8),
                import_notes="ALDI sagt Danke"),
        ], filename)

        call_command('import_transactions', filename, stdout=self.stdout)

        self.assertEqual(1, Transaction.objects.count())
        transaction = Transaction.objects.get()
        self.assertEqual(Decimal('-1234.56'), transaction.amount)
        self.assertEqual(datetime.date(2013, 2, 8), transaction.date)
        self.assertEqual("ALDI sagt Danke", transaction.import_notes)

    def test_re_import(self):
        kwargs = dict(
            date=datetime.datetime(2013, 1, 28),
            amount=Decimal('-21.95'), import_notes="Whatever")
        self.factory.make_one(Transaction, **kwargs)
        filename = os.path.join(self.tmp_dir, 'mytrans.csv')
        write_csv_transactions([
            self.factory.prepare_one(Transaction, **kwargs),
        ], filename)

        call_command('import_transactions', filename, stdout=self.stdout)

        self.assertEqual(1, Transaction.objects.count())

    def test_default_category(self):
        category = self.factory.make_one(Category)
        self.factory.make_one(Account)
        self.factory.make_one(TransactionCategoryHint,
                              import_notes_like='ALDI',
                              category=category)
        filename = os.path.join(self.tmp_dir, 'mytrans.csv')
        write_csv_transactions([
            self.factory.prepare_one(
                Transaction, amount=Decimal('-1234.56'),
                date=datetime.datetime(2013, 2, 8),
                import_notes="This ALDI sagt Danke"),
        ], filename)

        call_command('import_transactions', filename, stdout=self.stdout)

        self.assertEqual(1, Transaction.objects.count())
        transaction = Transaction.objects.get()
        self.assertEqual(category, transaction.category)

    def test_re_import_null_category(self):
        """A previously imported transaction with null category is updated."""
        kwargs = dict(
            date=datetime.datetime(2013, 1, 28),
            amount=Decimal('-21.95'), import_notes="Whatever")
        transaction = self.factory.make_one(Transaction, category=None,
                                            **kwargs)
        filename = os.path.join(self.tmp_dir, 'mytrans.csv')
        write_csv_transactions([
            self.factory.prepare_one(Transaction, **kwargs),
        ], filename)
        category = self.factory.make_one(Category)
        self.factory.make_one(TransactionCategoryHint,
                              import_notes_like='hateve',
                              category=category)

        call_command('import_transactions', filename, stdout=self.stdout)

        self.assertEqual(1, Transaction.objects.count())
        transaction = Transaction.objects.get()
        self.assertEqual(category, transaction.category)

    def make_transactions_file(self, filename, transactions=None):
        transactions = transactions or []
        filepath = os.path.join(self.tmp_dir, filename)
        write_csv_transactions(transactions, filepath)
        return filepath

    def test_non_existing_account_raises_error(self):
        filepath = self.make_transactions_file('mytrans.csv')

        self.assertRaises(
            CommandError, Command().handle, filepath, account_number=26)

    def test_existing_account_is_associated_with_trans(self):
        account = self.factory.make_one(Account)
        filepath = self.make_transactions_file(
            'mytrans.csv', transactions=[
                self.factory.prepare_one(Transaction),
            ])

        call_command('import_transactions', filepath,
                     account_number=account.id, stdout=self.stdout)

        transactions = Transaction.objects.all()
        self.assertEqual(1, transactions.count())
        self.assertEqual(account, transactions[0].account)
