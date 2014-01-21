# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Hardware.computersEnabledIn'
        db.alter_column(u'scraper_hardware', 'computersEnabledIn', self.gf('django.db.models.fields.CharField')(max_length=2000, null=True))

        # Changing field 'Hardware.computersCertifiedIn'
        db.alter_column(u'scraper_hardware', 'computersCertifiedIn', self.gf('django.db.models.fields.CharField')(max_length=2000, null=True))

        # Changing field 'Computer.parts'
        db.alter_column(u'scraper_computer', 'parts', self.gf('django.db.models.fields.CharField')(max_length=2000, null=True))

    def backwards(self, orm):

        # Changing field 'Hardware.computersEnabledIn'
        db.alter_column(u'scraper_hardware', 'computersEnabledIn', self.gf('separatedvaluesfield.models.SeparatedValuesField')(max_length=1000, null=True))

        # Changing field 'Hardware.computersCertifiedIn'
        db.alter_column(u'scraper_hardware', 'computersCertifiedIn', self.gf('separatedvaluesfield.models.SeparatedValuesField')(max_length=1000, null=True))

        # Changing field 'Computer.parts'
        db.alter_column(u'scraper_computer', 'parts', self.gf('separatedvaluesfield.models.SeparatedValuesField')(max_length=1000, null=True))

    models = {
        u'scraper.computer': {
            'Meta': {'object_name': 'Computer'},
            'certified': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'parts': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'scraper.hardware': {
            'Meta': {'object_name': 'Hardware'},
            'computersCertifiedIn': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True'}),
            'computersEnabledIn': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['scraper']