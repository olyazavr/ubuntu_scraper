# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Hardware.source'
        db.add_column(u'scraper_hardware', 'source',
                      self.gf('django.db.models.fields.CharField')(default='Ubuntu', max_length=200),
                      keep_default=False)

        # Adding field 'Computer.source'
        db.add_column(u'scraper_computer', 'source',
                      self.gf('django.db.models.fields.CharField')(default='Ubuntu', max_length=200),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Hardware.source'
        db.delete_column(u'scraper_hardware', 'source')

        # Deleting field 'Computer.source'
        db.delete_column(u'scraper_computer', 'source')


    models = {
        u'scraper.computer': {
            'Meta': {'object_name': 'Computer'},
            'certified': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'parts': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'scraper.hardware': {
            'Meta': {'object_name': 'Hardware'},
            'computersCertifiedIn': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True'}),
            'computersEnabledIn': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['scraper']