# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Computer.cid'
        db.delete_column(u'scraper_computer', 'cid')


    def backwards(self, orm):
        # Adding field 'Computer.cid'
        db.add_column(u'scraper_computer', 'cid',
                      self.gf('django.db.models.fields.CharField')(default='0', max_length=200),
                      keep_default=False)


    models = {
        u'scraper.computer': {
            'Meta': {'object_name': 'Computer'},
            'certified': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'parts': ('separatedvaluesfield.models.SeparatedValuesField', [], {'max_length': '1000', 'null': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'scraper.hardware': {
            'Meta': {'object_name': 'Hardware'},
            'computersCertifiedIn': ('separatedvaluesfield.models.SeparatedValuesField', [], {'max_length': '1000', 'null': 'True'}),
            'computersEnabledIn': ('separatedvaluesfield.models.SeparatedValuesField', [], {'max_length': '1000', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['scraper']