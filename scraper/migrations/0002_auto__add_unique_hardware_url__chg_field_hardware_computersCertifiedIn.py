# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'Hardware', fields ['url']
        db.create_unique(u'scraper_hardware', ['url'])


        # Changing field 'Hardware.computersCertifiedIn'
        db.alter_column(u'scraper_hardware', 'computersCertifiedIn', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Hardware.computersEnabledIn'
        db.alter_column(u'scraper_hardware', 'computersEnabledIn', self.gf('django.db.models.fields.TextField')(null=True))
        # Adding unique constraint on 'Computer', fields ['url']
        db.create_unique(u'scraper_computer', ['url'])


        # Changing field 'Computer.parts'
        db.alter_column(u'scraper_computer', 'parts', self.gf('django.db.models.fields.TextField')(null=True))

    def backwards(self, orm):
        # Removing unique constraint on 'Computer', fields ['url']
        db.delete_unique(u'scraper_computer', ['url'])

        # Removing unique constraint on 'Hardware', fields ['url']
        db.delete_unique(u'scraper_hardware', ['url'])


        # Changing field 'Hardware.computersCertifiedIn'
        db.alter_column(u'scraper_hardware', 'computersCertifiedIn', self.gf('django.db.models.fields.CharField')(max_length=2000, null=True))

        # Changing field 'Hardware.computersEnabledIn'
        db.alter_column(u'scraper_hardware', 'computersEnabledIn', self.gf('django.db.models.fields.CharField')(max_length=2000, null=True))

        # Changing field 'Computer.parts'
        db.alter_column(u'scraper_computer', 'parts', self.gf('django.db.models.fields.CharField')(max_length=2000000, null=True))

    models = {
        u'scraper.computer': {
            'Meta': {'object_name': 'Computer'},
            'certified': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'parts': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'scraper.hardware': {
            'Meta': {'object_name': 'Hardware'},
            'computersCertifiedIn': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'computersEnabledIn': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'})
        }
    }

    complete_apps = ['scraper']