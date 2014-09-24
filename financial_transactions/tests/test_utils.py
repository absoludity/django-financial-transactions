import datetime
from StringIO import StringIO
from decimal import Decimal

from categories.models import Category
from django_factory import TestCase
from ofxparse.ofxparse import (
    Account as OFXAccount,
    Ofx,
    Transaction as OFXTransaction,
    Statement as OFXStatement,
)

from financial_transactions.models import (
    Account,
    Transaction,
    TransactionCategoryHint,
)
from financial_transactions.utils import import_ofx


def ofx_transaction_for_transaction(transaction):
    ofx_transaction = OFXTransaction()
    ofx_transaction.date = transaction.date
    ofx_transaction.memo = transaction.memo
    ofx_transaction.amount = transaction.amount
    ofx_transaction.id = transaction.tid
    return ofx_transaction


def transactions_to_ofx_data(transactions, account):
    ofx_transactions = [
        ofx_transaction_for_transaction(t) for t in transactions]
    statement = OFXStatement()
    statement.transactions = ofx_transactions
    ofx_account = OFXAccount()
    ofx_account.statement = statement
    ofx_account.account_id = account.account_id
    ofx = Ofx()
    ofx.accounts = [ofx_account]
    return ofx


class ImportOFXTestCase(TestCase):

    def setUp(self):
        super(ImportOFXTestCase, self).setUp()

        self.stdout = StringIO()

    def test_creates_transactions(self):
        account = self.factory.make_one(Account)
        transactions = self.factory.prepare(5, Transaction, account=account)

        ofx = transactions_to_ofx_data(transactions, account)

        import_ofx(ofx, stdout=self.stdout)

        self.assertEqual(5, Transaction.objects.count())

    def test_transaction_values(self):
        account = self.factory.make_one(Account)
        transaction = self.factory.prepare_one(
            Transaction, amount=Decimal('-1234.56'),
            date=datetime.datetime(2013, 2, 8),
            memo="ALDI sagt Danke")
        ofx = transactions_to_ofx_data([transaction], account)

        import_ofx(ofx, stdout=self.stdout)

        self.assertEqual(1, Transaction.objects.count())
        transaction = Transaction.objects.get()
        self.assertEqual(Decimal('-1234.56'), transaction.amount)
        self.assertEqual(datetime.date(2013, 2, 8), transaction.date)
        self.assertEqual("ALDI sagt Danke", transaction.memo)

    def test_re_import(self):
        account = self.factory.make_one(Account, account_id="123C")
        kwargs = dict(
            date=datetime.datetime(2013, 1, 28),
            amount=Decimal('-21.95'), memo="Whatever",
            tid="abc123", account=account)
        transaction = self.factory.make_one(Transaction, **kwargs)
        ofx = transactions_to_ofx_data([transaction], account)

        import_ofx(ofx, stdout=self.stdout)

        self.assertEqual(1, Transaction.objects.count())

#    def test_default_category(self):
#        category = self.factory.make_one(Category)
#        self.factory.make_one(Account)
#        self.factory.make_one(TransactionCategoryHint,
#                              memo_like='ALDI',
#                              category=category)
#        filename = os.path.join(self.tmp_dir, 'mytrans.csv')
#        write_csv_transactions([
#            self.factory.prepare_one(
#                Transaction, amount=Decimal('-1234.56'),
#                date=datetime.datetime(2013, 2, 8),
#                memo="This ALDI sagt Danke"),
#        ], filename)
#
#        call_command('import_csvs', filename, stdout=self.stdout)
#
#        self.assertEqual(1, Transaction.objects.count())
#        transaction = Transaction.objects.get()
#        self.assertEqual(category, transaction.category)
#
#    def test_re_import_null_category(self):
#        """A previously imported transaction with null category is updated."""
#        kwargs = dict(
#            date=datetime.datetime(2013, 1, 28),
#            amount=Decimal('-21.95'), memo="Whatever")
#        transaction = self.factory.make_one(Transaction, category=None,
#                                            **kwargs)
#        filename = os.path.join(self.tmp_dir, 'mytrans.csv')
#        write_csv_transactions([
#            self.factory.prepare_one(Transaction, **kwargs),
#        ], filename)
#        category = self.factory.make_one(Category)
#        self.factory.make_one(TransactionCategoryHint,
#                              memo_like='hateve',
#                              category=category)
#
#        call_command('import_csvs', filename, stdout=self.stdout)
#
#        self.assertEqual(1, Transaction.objects.count())
#        transaction = Transaction.objects.get()
#        self.assertEqual(category, transaction.category)
#
#    def make_transactions_file(self, filename, transactions=None):
#        transactions = transactions or []
#        filepath = os.path.join(self.tmp_dir, filename)
#        write_csv_transactions(transactions, filepath)
#        return filepath
#
#    def test_non_existing_account_raises_error(self):
#        filepath = self.make_transactions_file('mytrans.csv')
#
#        self.assertRaises(
#            CommandError, Command().handle, filepath, account_number=26)
#
#    def test_existing_account_is_associated_with_trans(self):
#        account = self.factory.make_one(Account)
#        filepath = self.make_transactions_file(
#            'mytrans.csv', transactions=[
#                self.factory.prepare_one(Transaction),
#            ])
#
#        call_command('import_csvs', filepath,
#                     account_number=account.id, stdout=self.stdout)
#
#        transactions = Transaction.objects.all()
#        self.assertEqual(1, transactions.count())
#        self.assertEqual(account, transactions[0].account)
