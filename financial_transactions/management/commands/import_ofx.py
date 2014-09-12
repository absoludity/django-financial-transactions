import os

from ofxparse import OfxParser

from django.core.management import (
    BaseCommand,
    CommandError,
)

from financial_transactions.utils import import_ofx


class Command(BaseCommand):
    help = u'Import transactions from a ofx.'
    args = u'filename.ofx'

    def handle(self, *args, **kwargs):
        if len(args) != 1:
            raise CommandError("The csv file is required.")
        filename = args[0]
        if not os.path.exists(filename):
            raise CommandError("The file {0} does not exist.".format(
                filename))

        ofx = OfxParser.parse(file(filename))

        import_ofx(ofx, self.stdout)
