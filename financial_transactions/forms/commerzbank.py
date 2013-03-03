from django import forms
from financial_transactions.forms import TransactionFormBase


class GiroTransactionForm(TransactionFormBase):

    locale = 'de-de'
    delimiter = ';'

    date = forms.DateField(input_formats=[
        '%d.%m.%Y', '%Y-%m-%d'])
    amount = forms.DecimalField(max_digits=11, decimal_places=2, localize=True)
    sign = forms.CharField(max_length=1)

    def row_to_data(self, row):
        date, import_notes, amount, sign = row
        return dict(
            date=date, import_notes=import_notes, amount=amount,
            sign=sign, currency='EUR')

    def clean(self):
        cleaned_data = self.cleaned_data
        sign = cleaned_data.get('sign')
        amount = cleaned_data.get('amount')
        if amount and sign == '-':
            cleaned_data['amount'] *= -1
        return cleaned_data


class MasterCardTransactionForm(TransactionFormBase):

    locale = 'de-de'
    delimiter = ';'

    date_on_receipt = forms.DateField(input_formats=[
        '%d.%m.%Y', '%Y-%m-%d'])
    date = forms.DateField(input_formats=[
        '%d.%m.%Y', '%Y-%m-%d'])
    amount = forms.DecimalField(max_digits=11, decimal_places=2, localize=True)
    sign = forms.CharField(max_length=1)
    foreign_amount = forms.DecimalField(max_digits=11, decimal_places=2,
                                        localize=True, required=False)
    foreign_sign = forms.CharField(max_length=1, required=False)

    def row_to_data(self, row):
        (date_on_receipt, date, import_notes, amount,
         currency, sign) = row[:6]

        if len(row) == 9:
            (foreign_amount, foreign_currency, foreign_sign) = row[6:]
        else:
            (foreign_amount, foreign_currency, foreign_sign) = (
                None, None, None)

        return dict(
            date_on_receipt=date_on_receipt, date=date,
            import_notes=import_notes, amount=amount,
            sign=sign, currency='EUR', foreign_amount=foreign_amount,
            foreign_currency=foreign_currency, foreign_sign=foreign_sign)

    def clean(self):
        cleaned_data = self.cleaned_data
        sign = cleaned_data.get('sign')
        amount = cleaned_data.get('amount')
        if amount and sign == '-':
            cleaned_data['amount'] *= -1

        foreign_sign = cleaned_data.get('foreign_sign')
        foreign_amount = cleaned_data.get('foreign_amount')
        if foreign_amount and foreign_sign == '-':
            cleaned_data['foreign_amount'] *= -1
        return cleaned_data
