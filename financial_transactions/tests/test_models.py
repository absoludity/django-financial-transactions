import datetime
from decimal import Decimal
from django_factory import TestCase

from financial_transactions.models import (
    Account,
    Transaction,
)
from financial_transactions.forms.commerzbank import (
    GiroTransactionForm,
    MasterCardTransactionForm,
)


class TransactionTestCase(TestCase):

    def test_unicode(self):
        trans = self.factory.make_one(
            Transaction, import_notes=u'Sublime purchase',
            date=datetime.date(2013, 2, 5), amount=Decimal('59.95'),
            currency=u'EUR')

        self.assertEqual(u'2013-02-05 59.95 EUR - Sublime purchase',
                         unicode(trans))

    def test_factory_makes_category(self):
        transaction = self.factory.make_one(Transaction)

        self.assertIsNotNone(transaction.category)


class AccountTestCase(TestCase):

    def test_transaction_form_class(self):
        cases = (
            ('financial_transactions.forms.commerzbank.GiroTransactionForm',
             GiroTransactionForm),
            ('financial_transactions.forms.commerzbank.MasterCardTransactionForm',
             MasterCardTransactionForm),
        )

        for (val, klass) in cases:
            account = self.factory.make_one(Account, transaction_format=val)

            self.assertEqual(klass, account.transaction_form)

    def test_transaction_from_class_bad_module(self):
        name = 'financial_transactions.forms.foobank.GiroTransactionForm'

        account = self.factory.prepare_one(Account, transaction_format=name)

        self.assertIsNone(account.transaction_form)

    def test_transaction_from_class_bad_class(self):
        name = 'financial_transactions.forms.commerzbank.FooTransactionForm'

        account = self.factory.prepare_one(Account, transaction_format=name)

        self.assertIsNone(account.transaction_form)
