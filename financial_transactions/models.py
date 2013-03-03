import importlib
from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from categories.models import Category


class Transaction(models.Model):
    date = models.DateField(_('Date'), default=now)
    date_on_receipt = models.DateField(_('Receipt date'), null=True,
                                       blank=True)
    amount = models.DecimalField(_('Amount'), max_digits=11,
                                 decimal_places=2)
    currency = models.CharField(_('Currency'), max_length=3)
    foreign_amount = models.DecimalField(_('Foreign amount'), max_digits=11,
                                         decimal_places=2, null=True,
                                         blank=True)
    foreign_currency = models.CharField(_('Foreign currency'), max_length=3,
                                        blank=True)
    import_notes = models.TextField(_('Import notes'))
    imported_at = models.DateTimeField(_('Imported at'),
                                       default=now)

    category = models.ForeignKey('categories.Category', null=True, blank=True)
    account = models.ForeignKey('Account')

    def __unicode__(self):
        return u"{date} {amount} {currency} - {import_notes}".format(
            amount=self.amount, currency=self.currency, date=self.date,
            import_notes=self.import_notes)

    class Factory:
        @staticmethod
        def get_category(field, factory):
            return factory.prepare_one(Category)


class TransactionCategoryHint(models.Model):
    """Automatically associate a transaction to a category."""
    category = models.ForeignKey('categories.Category')
    import_notes_like = models.CharField(max_length=255)


class Account(models.Model):
    name = models.CharField(max_length=31)
    # XXX Forms should register themselves or similar.
    transaction_format = models.CharField(max_length=255, choices=(
        ('financial_transactions.forms.commerzbank.GiroTransactionForm',
         'CommerzBank Giro'),
        ('financial_transactions.forms.commerzbank.MasterCardTransactionForm',
         'CommerzBank MasterCard'),
        ))

    def __unicode__(self):
        return self.name

    @property
    def transaction_form(self):
        module, _, klass = self.transaction_format.rpartition('.')
        try:
            module = importlib.import_module(module)
        except ImportError:
            return None

        return getattr(module, klass, None)

    class Meta:
        ordering = ['id']

    class Factory:
        @staticmethod
        def get_transaction_format(field, factory):
            return 'financial_transactions.forms.commerzbank.GiroTransactionForm'
