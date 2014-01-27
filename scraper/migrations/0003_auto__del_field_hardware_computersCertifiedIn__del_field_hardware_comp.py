# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Hardware', fields ['url']
        db.delete_unique(u'scraper_hardware', ['url'])

        # Deleting field 'Hardware.computersCertifiedIn'
        db.delete_column(u'scraper_hardware', 'computersCertifiedIn')

        # Deleting field 'Hardware.computersEnabledIn'
        db.delete_column(u'scraper_hardware', 'computersEnabledIn')

        # Adding M2M table for field computersCertifiedIn on 'Hardware'
        db.create_table(u'scraper_hardware_computersCertifiedIn', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('hardware', models.ForeignKey(orm[u'scraper.hardware'], null=False)),
            ('computer', models.ForeignKey(orm[u'scraper.computer'], null=False))
        ))
        db.create_unique(u'scraper_hardware_computersCertifiedIn', ['hardware_id', 'computer_id'])

        # Adding M2M table for field computersEnabledIn on 'Hardware'
        db.create_table(u'scraper_hardware_computersEnabledIn', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('hardware', models.ForeignKey(orm[u'scraper.hardware'], null=False)),
            ('computer', models.ForeignKey(orm[u'scraper.computer'], null=False))
        ))
        db.create_unique(u'scraper_hardware_computersEnabledIn', ['hardware_id', 'computer_id'])


        # Changing field 'Hardware.url'
        db.alter_column(u'scraper_hardware', 'url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True))
        # Deleting field 'Computer.parts'
        db.delete_column(u'scraper_computer', 'parts')


    def backwards(self, orm):
        # Adding field 'Hardware.computersCertifiedIn'
        db.add_column(u'scraper_hardware', 'computersCertifiedIn',
                      self.gf('django.db.models.fields.TextField')(null=True),
                      keep_default=False)

        # Adding field 'Hardware.computersEnabledIn'
        db.add_column(u'scraper_hardware', 'computersEnabledIn',
                      self.gf('django.db.models.fields.TextField')(null=True),
                      keep_default=False)

        # Removing M2M table for field computersCertifiedIn on 'Hardware'
        db.delete_table('scraper_hardware_computersCertifiedIn')

        # Removing M2M table for field computersEnabledIn on 'Hardware'
        db.delete_table('scraper_hardware_computersEnabledIn')


        # Changing field 'Hardware.url'
        db.alter_column(u'scraper_hardware', 'url', self.gf('django.db.models.fields.URLField')(default='Unknown', max_length=200, unique=True))
        # Adding unique constraint on 'Hardware', fields ['url']
        db.create_unique(u'scraper_hardware', ['url'])

        # Adding field 'Computer.parts'
        db.add_column(u'scraper_computer', 'parts',
                      self.gf('django.db.models.fields.TextField')(null=True),
                      keep_default=False)


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
        }
    }

    complete_apps = ['scraper']