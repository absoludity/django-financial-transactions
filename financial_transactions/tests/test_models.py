import datetime
from decimal import Decimal
from django_factory import TestCase

from financial_transactions.models import (
    Transaction,
)


class TransactionTestCase(TestCase):

    def test_unicode(self):
        trans = self.factory.make_one(
            Transaction, memo=u'Sublime purchase',
            date=datetime.date(2013, 2, 5), amount=Decimal('59.95'),
            currency=u'EUR')

        self.assertEqual(u'2013-02-05 59.95 EUR - Sublime purchase',
                         unicode(trans))

    def test_factory_makes_category(self):
        transaction = self.factory.make_one(Transaction)

        self.assertIsNotNone(transaction.category)
