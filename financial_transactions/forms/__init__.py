from django import forms
from financial_transactions.models import Transaction


class TransactionFormBase(forms.ModelForm):

    locale = None
    delimiter = ','

    def __init__(self, row, account):
        data = self.row_to_data(row)
        data['account'] = account.id
        return super(TransactionFormBase, self).__init__(data)

    def row_to_data(self, row):
        raise NotImplemented("TransactionForm subclasses must define the "
                             "form data based on the row.")

    class Meta:
        model = Transaction
        exclude = ('imported_at', 'category')
