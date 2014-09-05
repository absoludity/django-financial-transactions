import datetime
from decimal import Decimal
from django.conf import settings
from django.utils import translation
from django_factory import TestCase

from financial_transactions.models import Account
from financial_transactions.forms.commerzbank import (
    GiroTransactionForm,
    MasterCardTransactionForm,
)


class GiroTransactionFormTestCase(TestCase):

    def setUp(self):
        super(GiroTransactionFormTestCase, self).setUp()
        translation.activate(GiroTransactionForm.locale)
        self.addCleanup(translation.activate, settings.LANGUAGE_CODE)

    def test_cleaned_amount_correct_sign(self):
        account = self.factory.make_one(Account)
        row = ['31.12.2012', 'Whatever', '5345,09', '-']
        f = GiroTransactionForm(row, account)

        is_valid = f.is_valid()

        self.assertTrue(is_valid)
        self.assertEqual(Decimal('-5345.09'), f.cleaned_data['amount'])
        self.assertEqual(datetime.date(2012, 12, 31), f.cleaned_data['date'])


class MasterCardTransactionFormTestCase(TestCase):

    def setUp(self):
        super(MasterCardTransactionFormTestCase, self).setUp()
        translation.activate(MasterCardTransactionForm.locale)
        self.addCleanup(translation.activate, settings.LANGUAGE_CODE)

    def test_clean(self):
        account = self.factory.make_one(Account)
        row = [
            '20.12.2012',
            '27.12.2012',
            'SKYPE 4444444444 444',
            '10,00', 'EUR', '-',
            '11,00', 'USD', '-',
        ]
        f = MasterCardTransactionForm(row, account)

        is_valid = f.is_valid()

        self.assertTrue(is_valid)
        self.assertEqual(datetime.date(2012, 12, 27), f.cleaned_data['date'])
        self.assertEqual(datetime.date(2012, 12, 20),
                         f.cleaned_data['date_on_receipt'])
        self.assertEqual(Decimal('-10.00'), f.cleaned_data['amount'])
        self.assertEqual('EUR', f.cleaned_data['currency'])
        self.assertEqual(Decimal('-11.00'), f.cleaned_data['foreign_amount'])
        self.assertEqual('USD', f.cleaned_data['foreign_currency'])

    def test_clean_lastschrifteinzug(self):
        account = self.factory.make_one(Account)
        row = [
            '27.12.2012',
            '27.12.2012',
            'LASTSCHRIFTEINZUG',
            '64,20', 'EUR', '+',
            '-',
        ]
        f = MasterCardTransactionForm(row, account)

        is_valid = f.is_valid()

        self.assertTrue(is_valid)
        self.assertEqual(datetime.date(2012, 12, 27), f.cleaned_data['date'])
        self.assertEqual(datetime.date(2012, 12, 27),
                         f.cleaned_data['date_on_receipt'])
        self.assertEqual(Decimal('64.20'), f.cleaned_data['amount'])
        self.assertEqual('EUR', f.cleaned_data['currency'])
        self.assertEqual(None, f.cleaned_data['foreign_amount'])
        self.assertEqual('', f.cleaned_data['foreign_currency'])
