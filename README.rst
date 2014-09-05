======================
Financial Transactions
======================

.. image:: https://travis-ci.org/absoludity/django-financial-transactions.svg?branch=master
    :target: https://travis-ci.org/absoludity/django-financial-transactions
        :alt: Build Status

Financial Transactions is a Django app to import and categorise transactions from financial institutions, where categories are assigned based on hints.

It's intended for hackers who want to build other interesting stuff with their categorised financial transactions.


Quick Start
-----------

1. Add "financial_transactions" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'financial_transactions',
    )

2. Run `python manage.py syncdb` to create the Financial Transaction models.

3. Start the development server and visit http://127.0.0.1:8000/admin/
to create an account (you'll need the Admin app enabled), choosing a transaction format for the account (currently only CommerzBank Giro and Commerzbank Mastercard csvs are supported, but I'll add forms as people need them.)

4. Import your transactions::

    ./manage.py import_transactions ~/mydata/2013-01-commerzbank.csv

You can then browse your transactions in the /admin/, add transaction category hints, and reimport your csvs to automatically update the categories based on your hints.
