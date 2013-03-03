# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Transaction'
        db.create_table('financial_transactions_transaction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime.now)),
            ('date_on_receipt', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=11, decimal_places=2)),
            ('currency', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('foreign_amount', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=11, decimal_places=2, blank=True)),
            ('foreign_currency', self.gf('django.db.models.fields.CharField')(max_length=3, blank=True)),
            ('import_notes', self.gf('django.db.models.fields.TextField')()),
            ('imported_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categories.Category'], null=True, blank=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['financial_transactions.Account'])),
        ))
        db.send_create_signal('financial_transactions', ['Transaction'])

        # Adding model 'TransactionCategoryHint'
        db.create_table('financial_transactions_transactioncategoryhint', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categories.Category'])),
            ('import_notes_like', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('financial_transactions', ['TransactionCategoryHint'])

        # Adding model 'Account'
        db.create_table('financial_transactions_account', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=31)),
            ('transaction_format', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('financial_transactions', ['Account'])


    def backwards(self, orm):
        # Deleting model 'Transaction'
        db.delete_table('financial_transactions_transaction')

        # Deleting model 'TransactionCategoryHint'
        db.delete_table('financial_transactions_transactioncategoryhint')

        # Deleting model 'Account'
        db.delete_table('financial_transactions_account')


    models = {
        'categories.category': {
            'Meta': {'ordering': "('tree_id', 'lft')", 'unique_together': "(('parent', 'name'),)", 'object_name': 'Category'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'alternate_title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'alternate_url': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'meta_extra': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'meta_keywords': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['categories.Category']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'thumbnail': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'thumbnail_height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'thumbnail_width': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'financial_transactions.account': {
            'Meta': {'ordering': "['id']", 'object_name': 'Account'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '31'}),
            'transaction_format': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'financial_transactions.transaction': {
            'Meta': {'object_name': 'Transaction'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['financial_transactions.Account']"}),
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '11', 'decimal_places': '2'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['categories.Category']", 'null': 'True', 'blank': 'True'}),
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now'}),
            'date_on_receipt': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'foreign_amount': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '11', 'decimal_places': '2', 'blank': 'True'}),
            'foreign_currency': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'import_notes': ('django.db.models.fields.TextField', [], {}),
            'imported_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        'financial_transactions.transactioncategoryhint': {
            'Meta': {'object_name': 'TransactionCategoryHint'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['categories.Category']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'import_notes_like': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['financial_transactions']