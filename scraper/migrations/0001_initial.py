# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Hardware'
        db.create_table(u'scraper_hardware', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('computersCertifiedIn', self.gf('separatedvaluesfield.models.SeparatedValuesField')(max_length=1000, null=True)),
            ('computersEnabledIn', self.gf('separatedvaluesfield.models.SeparatedValuesField')(max_length=1000, null=True)),
        ))
        db.send_create_signal(u'scraper', ['Hardware'])

        # Adding model 'Computer'
        db.create_table(u'scraper_computer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('cid', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('certified', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('parts', self.gf('separatedvaluesfield.models.SeparatedValuesField')(max_length=1000, null=True)),
        ))
        db.send_create_signal(u'scraper', ['Computer'])


    def backwards(self, orm):
        # Deleting model 'Hardware'
        db.delete_table(u'scraper_hardware')

        # Deleting model 'Computer'
        db.delete_table(u'scraper_computer')


    models = {
        u'scraper.computer': {
            'Meta': {'object_name': 'Computer'},
            'certified': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'cid': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
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