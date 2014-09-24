from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from categories.models import Category


class Transaction(models.Model):
    tid = models.TextField()
    date = models.DateField(_('Date'))
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
    memo = models.TextField(_('Memo'))
    imported_at = models.DateTimeField(_('Imported at'),
                                       default=now)

    category = models.ForeignKey('categories.Category', null=True, blank=True)
    account = models.ForeignKey('Account')

    class Meta:
        unique_together = (('id', 'account'),)

    def __unicode__(self):
        return u"{date} {amount} {currency} - {memo}".format(
            amount=self.amount, currency=self.currency, date=self.date,
            memo=self.memo)

    class Factory:
        @staticmethod
        def get_category(field, factory):
            return factory.prepare_one(Category)


class TransactionCategoryHint(models.Model):
    """Automatically associate a transaction to a category."""
    category = models.ForeignKey('categories.Category')
    memo_like = models.CharField(max_length=255)


class Account(models.Model):
    account_id = models.CharField(max_length=31)
    name = models.CharField(max_length=31)

    class Meta:
        ordering = ['account_id']

    def __unicode__(self):
        return u"{name} ({id})".format(
            name=self.name, id=self.account_id)
