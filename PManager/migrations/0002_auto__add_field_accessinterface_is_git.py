# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'AccessInterface.is_git'
        db.add_column(u'PManager_accessinterface', 'is_git',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'AccessInterface.is_git'
        db.delete_column(u'PManager_accessinterface', 'is_git')


    models = {
        'PManager.accessinterface': {
            'Meta': {'object_name': 'AccessInterface'},
            'access_roles': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'file_categories'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['PManager.PM_Role']"}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_git': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'port': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['PManager.PM_Project']"}),
            'protocol': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        },
        'PManager.agent': {
            'Meta': {'object_name': 'Agent'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_process_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'last_result_message': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'once': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'required': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'seconds': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'PManager.credit': {
            'Meta': {'object_name': 'Credit'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payer': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'credits'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'credits'", 'null': 'True', 'to': "orm['PManager.PM_Project']"}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'costs'", 'null': 'True', 'to': "orm['PManager.PM_Task']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'arrears'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'PManager.key': {
            'Meta': {'object_name': 'Key'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'file_path': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key_data': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        'PManager.logdata': {
            'Meta': {'object_name': 'LogData'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'PManager.objecttags': {
            'Meta': {'object_name': 'ObjectTags'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'objectLinks'", 'to': "orm['PManager.Tags']"}),
            'weight': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'PManager.payment': {
            'Meta': {'object_name': 'Payment'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payer': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'repayments'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'payments'", 'null': 'True', 'to': "orm['PManager.PM_Project']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'payments'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'PManager.pm_achievement': {
            'Meta': {'object_name': 'PM_Achievement'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'condition': ('django.db.models.fields.TextField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'PManager.pm_file_category': {
            'Meta': {'object_name': 'PM_File_Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['PManager.PM_File_Category']"}),
            'projects': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'file_categories'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['PManager.PM_Project']"})
        },
        'PManager.pm_files': {
            'Meta': {'object_name': 'PM_Files'},
            'authorId': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'files'", 'null': 'True', 'to': "orm['PManager.PM_File_Category']"}),
            'date_create': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '400'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_old_version': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'projectId': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['PManager.PM_Project']", 'null': 'True'}),
            'versions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'versions_rel_+'", 'null': 'True', 'to': "orm['PManager.PM_Files']"})
        },
        'PManager.pm_milestone': {
            'Meta': {'object_name': 'PM_Milestone'},
            'closed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'critically': ('django.db.models.fields.IntegerField', [], {'default': '2', 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_create': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'overdue': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'milestones'", 'to': "orm['PManager.PM_Project']"}),
            'responsible': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'PManager.pm_notice': {
            'Meta': {'object_name': 'PM_Notice'},
            'html': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'itemClass': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'PManager.pm_noticedusers': {
            'Meta': {'object_name': 'PM_NoticedUsers'},
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 11, 14, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notice': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'userNotices'", 'to': "orm['PManager.PM_Notice']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notices'", 'to': u"orm['auth.User']"})
        },
        'PManager.pm_project': {
            'Meta': {'object_name': 'PM_Project'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'createdProjects'", 'to': u"orm['auth.User']"}),
            'closed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'repository': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'settings': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'tracker': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'projects'", 'to': "orm['PManager.PM_Tracker']"})
        },
        'PManager.pm_projectroles': {
            'Meta': {'object_name': 'PM_ProjectRoles'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payment_type': ('django.db.models.fields.CharField', [], {'default': "'real_time'", 'max_length': '100'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'projectRoles'", 'to': "orm['PManager.PM_Project']"}),
            'rate': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['PManager.PM_Role']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'userRoles'", 'to': u"orm['auth.User']"})
        },
        'PManager.pm_properties': {
            'Meta': {'object_name': 'PM_Properties'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'PManager.pm_property_values': {
            'Meta': {'object_name': 'PM_Property_Values'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'propertyId': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['PManager.PM_Properties']"}),
            'taskId': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['PManager.PM_Task']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '1000'})
        },
        'PManager.pm_role': {
            'Meta': {'object_name': 'PM_Role'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'tracker': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['PManager.PM_Tracker']"})
        },
        'PManager.pm_task': {
            'Meta': {'object_name': 'PM_Task'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'createdTasks'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'closed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'critically': ('django.db.models.fields.FloatField', [], {'default': '0.5'}),
            'dateClose': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'dateStart': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'deadline': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'files': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'fileTasks'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['PManager.PM_Files']"}),
            'hardness': ('django.db.models.fields.FloatField', [], {'default': '0.5'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'milestone': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tasks'", 'null': 'True', 'to': "orm['PManager.PM_Milestone']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'observers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'tasksLooking'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'onPlanning': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'parentTask': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'subTasks'", 'null': 'True', 'to': "orm['PManager.PM_Task']"}),
            'perhapsResponsible': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'hisTasksMaybe'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'planTime': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'priority': ('django.db.models.fields.FloatField', [], {'default': '0.5'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'projectTasks'", 'null': 'True', 'to': "orm['PManager.PM_Project']"}),
            'project_knowledge': ('django.db.models.fields.FloatField', [], {'default': '0.5'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'realDateStart': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'realTime': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'reconcilement': ('django.db.models.fields.FloatField', [], {'default': '0.5'}),
            'resp': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'todo'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'responsible': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'hisTasks'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'started': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tasksByStatus'", 'null': 'True', 'to': "orm['PManager.PM_Task_Status']"}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'viewedUsers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'virgin': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'wasClosed': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'PManager.pm_task_message': {
            'Meta': {'object_name': 'PM_Task_Message'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'outputMessages'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'files': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'msgTasks'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['PManager.PM_Files']"}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hidden_from_clients': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hidden_from_employee': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isSystemLog': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['PManager.PM_Project']", 'null': 'True'}),
            'read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'messages'", 'null': 'True', 'to': "orm['PManager.PM_Task']"}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '10000'}),
            'userTo': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'incomingMessages'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        'PManager.pm_task_status': {
            'Meta': {'object_name': 'PM_Task_Status'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'PManager.pm_timer': {
            'Meta': {'object_name': 'PM_Timer'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'dateEnd': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'dateStart': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'seconds': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['PManager.PM_Task']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        'PManager.pm_tracker': {
            'Meta': {'object_name': 'PM_Tracker'},
            'admin': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'createdTrackers'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'PManager.pm_user': {
            'Meta': {'object_name': 'PM_User'},
            'account_total': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'avatar_color': ('django.db.models.fields.CharField', [], {'default': "'#cd5555'", 'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'birthday': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'icq': ('django.db.models.fields.CharField', [], {'max_length': '70', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_outsource': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_activity_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'paid': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'rating': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'skype': ('django.db.models.fields.CharField', [], {'max_length': '70', 'null': 'True', 'blank': 'True'}),
            'sp_price': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'specialties': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'profiles'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['PManager.Specialty']"}),
            'specialty': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['PManager.Specialty']", 'null': 'True', 'blank': 'True'}),
            'trackers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['PManager.PM_Tracker']", 'null': 'True', 'symmetrical': 'False'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        'PManager.pm_user_achievement': {
            'Meta': {'object_name': 'PM_User_Achievement'},
            'achievement': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'achievement_users'", 'to': "orm['PManager.PM_Achievement']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_achievements'", 'to': u"orm['auth.User']"})
        },
        'PManager.pm_user_plantime': {
            'Meta': {'object_name': 'PM_User_PlanTime'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['PManager.PM_Task']"}),
            'time': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        'PManager.specialty': {
            'Meta': {'object_name': 'Specialty'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'PManager.tags': {
            'Meta': {'object_name': 'Tags'},
            'frequency': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tagText': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['PManager']