# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Transaction'
        db.create_table(u'financial_transactions_transaction', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tid', self.gf('django.db.models.fields.TextField')()),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('date_on_receipt', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=11, decimal_places=2)),
            ('currency', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('foreign_amount', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=11, decimal_places=2, blank=True)),
            ('foreign_currency', self.gf('django.db.models.fields.CharField')(max_length=3, blank=True)),
            ('memo', self.gf('django.db.models.fields.TextField')()),
            ('imported_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categories.Category'], null=True, blank=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['financial_transactions.Account'])),
        ))
        db.send_create_signal(u'financial_transactions', ['Transaction'])

        # Adding unique constraint on 'Transaction', fields [u'id', 'account']
        db.create_unique(u'financial_transactions_transaction', [u'id', 'account_id'])

        # Adding model 'TransactionCategoryHint'
        db.create_table(u'financial_transactions_transactioncategoryhint', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categories.Category'])),
            ('memo_like', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'financial_transactions', ['TransactionCategoryHint'])

        # Adding model 'Account'
        db.create_table(u'financial_transactions_account', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('account_id', self.gf('django.db.models.fields.CharField')(max_length=31)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=31)),
        ))
        db.send_create_signal(u'financial_transactions', ['Account'])


    def backwards(self, orm):
        # Removing unique constraint on 'Transaction', fields [u'id', 'account']
        db.delete_unique(u'financial_transactions_transaction', [u'id', 'account_id'])

        # Deleting model 'Transaction'
        db.delete_table(u'financial_transactions_transaction')

        # Deleting model 'TransactionCategoryHint'
        db.delete_table(u'financial_transactions_transactioncategoryhint')

        # Deleting model 'Account'
        db.delete_table(u'financial_transactions_account')


    models = {
        u'categories.category': {
            'Meta': {'ordering': "('tree_id', 'lft')", 'unique_together': "(('parent', 'name'),)", 'object_name': 'Category'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'alternate_title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'alternate_url': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'meta_extra': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'meta_keywords': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['categories.Category']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'thumbnail': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'thumbnail_height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'thumbnail_width': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        u'financial_transactions.account': {
            'Meta': {'ordering': "['account_id']", 'object_name': 'Account'},
            'account_id': ('django.db.models.fields.CharField', [], {'max_length': '31'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '31'})
        },
        u'financial_transactions.transaction': {
            'Meta': {'unique_together': "(('id', 'account'),)", 'object_name': 'Transaction'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['financial_transactions.Account']"}),
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '11', 'decimal_places': '2'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categories.Category']", 'null': 'True', 'blank': 'True'}),
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'date_on_receipt': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'foreign_amount': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '11', 'decimal_places': '2', 'blank': 'True'}),
            'foreign_currency': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imported_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'memo': ('django.db.models.fields.TextField', [], {}),
            'tid': ('django.db.models.fields.TextField', [], {})
        },
        u'financial_transactions.transactioncategoryhint': {
            'Meta': {'object_name': 'TransactionCategoryHint'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categories.Category']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'memo_like': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['financial_transactions']