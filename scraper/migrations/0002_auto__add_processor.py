# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Processor'
        db.create_table(u'scraper_processor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(unique=True, max_length=200)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('codename', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('graphics', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'scraper', ['Processor'])


    def backwards(self, orm):
        # Deleting model 'Processor'
        db.delete_table(u'scraper_processor')


    models = {
        u'scraper.computer': {
            'Meta': {'object_name': 'Computer'},
            'certified': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'scraper.hardware': {
            'Meta': {'object_name': 'Hardware'},
            'computersCertifiedIn': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'certifiedIn'", 'symmetrical': 'False', 'to': u"orm['scraper.Computer']"}),
            'computersEnabledIn': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'enabledIn'", 'symmetrical': 'False', 'to': u"orm['scraper.Computer']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'})
        },
        u'scraper.processor': {
            'Meta': {'object_name': 'Processor'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'graphics': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'})
        }
    }

    complete_apps = ['scraper']