import os

from ofxparse import OfxParser

from django.core.management import (
    BaseCommand,
    CommandError,
)

from financial_transactions.utils import import_ofx


class Command(BaseCommand):
    help = u'Import transactions from all ofx files in specified directory.'
    args = u'/path/to/ofxes'

    def handle(self, *args, **kwargs):
        if len(args) != 1:
            raise CommandError("The directory containing the ofx files is required.")
        directory = args[0]
        if not os.path.exists(directory):
            raise CommandError("The directory {0} does not exist.".format(
                directory))

        for filename in os.listdir(directory):
            if filename.endswith(".ofx") or filename.endswith("OFX"):
                filepath = os.path.join(directory, filename)
                ofx = OfxParser.parse(file(filepath))
                self.stdout.write("Importing {}...".format(filename))
                import_ofx(ofx, self.stdout)
