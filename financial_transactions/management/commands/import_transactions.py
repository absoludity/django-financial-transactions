import os
from django.core.management import (
    BaseCommand,
    CommandError,
)
from optparse import make_option

from financial_transactions.models import Account
from financial_transactions.utils import import_csv


accounts = Account.objects.order_by('id').values_list(
    'id', 'name')
accounts = ["{0} ({1})".format(id, name) for id, name in accounts]
accounts = ', '.join(accounts)


class Command(BaseCommand):
    help = u'Import transactions from a csv.'
    args = u'filename.csv'

    option_list = BaseCommand.option_list + (
        make_option('--account-number',
                    help=u'The account for the transactions. '
                         u'Current options: {0}'.format(accounts)),
    )

    def handle(self, *args, **kwargs):
        if len(args) != 1:
            raise CommandError("The csv file is required.")
        filename = args[0]
        if not os.path.exists(filename):
            raise CommandError("The file {0} does not exist.".format(
                filename))

        account_num = kwargs.get('account_number')
        if not account_num:
            account = Account.objects.order_by('id')[0]
        else:
            try:
                account = Account.objects.get(pk=account_num)
            except Account.DoesNotExist:
                raise CommandError(
                    "There is no account with the number {0}. "
                    "Current accounts are: {1}.".format(
                        account_num, accounts))

        import_csv(filename, account.transaction_form, account,
                   self.stdout)
