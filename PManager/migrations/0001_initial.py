# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tags'
        db.create_table(u'PManager_tags', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tagText', self.gf('django.db.models.fields.CharField')(max_length=100, db_index=True)),
            ('frequency', self.gf('django.db.models.fields.FloatField')(default=0)),
        ))
        db.send_create_signal('PManager', ['Tags'])

        # Adding model 'ObjectTags'
        db.create_table(u'PManager_objecttags', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(related_name='objectLinks', to=orm['PManager.Tags'])),
            ('weight', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('PManager', ['ObjectTags'])

        # Adding model 'PM_Tracker'
        db.create_table(u'PManager_pm_tracker', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('dateCreate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True)),
            ('admin', self.gf('django.db.models.fields.related.ForeignKey')(related_name='createdTrackers', null=True, to=orm['auth.User'])),
            ('logo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True)),
        ))
        db.send_create_signal('PManager', ['PM_Tracker'])

        # Adding model 'PM_Project'
        db.create_table(u'PManager_pm_project', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('dateCreate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='createdProjects', to=orm['auth.User'])),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True)),
            ('tracker', self.gf('django.db.models.fields.related.ForeignKey')(related_name='projects', to=orm['PManager.PM_Tracker'])),
            ('repository', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('closed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('settings', self.gf('django.db.models.fields.CharField')(max_length=1000)),
        ))
        db.send_create_signal('PManager', ['PM_Project'])

        # Adding model 'PM_File_Category'
        db.create_table(u'PManager_pm_file_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='children', null=True, to=orm['PManager.PM_File_Category'])),
        ))
        db.send_create_signal('PManager', ['PM_File_Category'])

        # Adding M2M table for field projects on 'PM_File_Category'
        m2m_table_name = db.shorten_name(u'PManager_pm_file_category_projects')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pm_file_category', models.ForeignKey(orm['PManager.pm_file_category'], null=False)),
            ('pm_project', models.ForeignKey(orm['PManager.pm_project'], null=False))
        ))
        db.create_unique(m2m_table_name, ['pm_file_category_id', 'pm_project_id'])

        # Adding model 'PM_Files'
        db.create_table(u'PManager_pm_files', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=400)),
            ('authorId', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            ('projectId', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['PManager.PM_Project'], null=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='files', null=True, to=orm['PManager.PM_File_Category'])),
            ('is_old_version', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('date_create', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
        ))
        db.send_create_signal('PManager', ['PM_Files'])

        # Adding M2M table for field versions on 'PM_Files'
        m2m_table_name = db.shorten_name(u'PManager_pm_files_versions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_pm_files', models.ForeignKey(orm['PManager.pm_files'], null=False)),
            ('to_pm_files', models.ForeignKey(orm['PManager.pm_files'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_pm_files_id', 'to_pm_files_id'])

        # Adding model 'PM_Task_Status'
        db.create_table(u'PManager_pm_task_status', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('PManager', ['PM_Task_Status'])

        # Adding model 'PM_Milestone'
        db.create_table(u'PManager_pm_milestone', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('date_create', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('critically', self.gf('django.db.models.fields.IntegerField')(default=2, null=True, blank=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(related_name='milestones', to=orm['PManager.PM_Project'])),
            ('overdue', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('closed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('PManager', ['PM_Milestone'])

        # Adding M2M table for field responsible on 'PM_Milestone'
        m2m_table_name = db.shorten_name(u'PManager_pm_milestone_responsible')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pm_milestone', models.ForeignKey(orm['PManager.pm_milestone'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['pm_milestone_id', 'user_id'])

        # Adding model 'PM_Task'
        db.create_table(u'PManager_pm_task', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='projectTasks', null=True, to=orm['PManager.PM_Project'])),
            ('resp', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='todo', null=True, to=orm['auth.User'])),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='createdTasks', null=True, to=orm['auth.User'])),
            ('status', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tasksByStatus', null=True, to=orm['PManager.PM_Task_Status'])),
            ('dateCreate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('dateModify', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('dateClose', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('dateStart', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('deadline', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('milestone', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tasks', null=True, to=orm['PManager.PM_Milestone'])),
            ('onPlanning', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('planTime', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('realTime', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('realDateStart', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('closed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('started', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('wasClosed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('priority', self.gf('django.db.models.fields.FloatField')(default=0.5)),
            ('critically', self.gf('django.db.models.fields.FloatField')(default=0.5)),
            ('hardness', self.gf('django.db.models.fields.FloatField')(default=0.5)),
            ('reconcilement', self.gf('django.db.models.fields.FloatField')(default=0.5)),
            ('project_knowledge', self.gf('django.db.models.fields.FloatField')(default=0.5)),
            ('parentTask', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='subTasks', null=True, to=orm['PManager.PM_Task'])),
            ('virgin', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('PManager', ['PM_Task'])

        # Adding M2M table for field responsible on 'PM_Task'
        m2m_table_name = db.shorten_name(u'PManager_pm_task_responsible')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pm_task', models.ForeignKey(orm['PManager.pm_task'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['pm_task_id', 'user_id'])

        # Adding M2M table for field observers on 'PM_Task'
        m2m_table_name = db.shorten_name(u'PManager_pm_task_observers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pm_task', models.ForeignKey(orm['PManager.pm_task'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['pm_task_id', 'user_id'])

        # Adding M2M table for field perhapsResponsible on 'PM_Task'
        m2m_table_name = db.shorten_name(u'PManager_pm_task_perhapsResponsible')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pm_task', models.ForeignKey(orm['PManager.pm_task'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['pm_task_id', 'user_id'])

        # Adding M2M table for field viewedUsers on 'PM_Task'
        m2m_table_name = db.shorten_name(u'PManager_pm_task_viewedUsers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pm_task', models.ForeignKey(orm['PManager.pm_task'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['pm_task_id', 'user_id'])

        # Adding M2M table for field files on 'PM_Task'
        m2m_table_name = db.shorten_name(u'PManager_pm_task_files')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pm_task', models.ForeignKey(orm['PManager.pm_task'], null=False)),
            ('pm_files', models.ForeignKey(orm['PManager.pm_files'], null=False))
        ))
        db.create_unique(m2m_table_name, ['pm_task_id', 'pm_files_id'])

        # Adding model 'PM_Timer'
        db.create_table(u'PManager_pm_timer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['PManager.PM_Task'])),
            ('dateStart', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('dateEnd', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('seconds', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('price', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal('PManager', ['PM_Timer'])

        # Adding model 'PM_Properties'
        db.create_table(u'PManager_pm_properties', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('PManager', ['PM_Properties'])

        # Adding model 'PM_Property_Values'
        db.create_table(u'PManager_pm_property_values', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('propertyId', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['PManager.PM_Properties'])),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('taskId', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['PManager.PM_Task'])),
        ))
        db.send_create_signal('PManager', ['PM_Property_Values'])

        # Adding model 'PM_Task_Message'
        db.create_table(u'PManager_pm_task_message', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=10000)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='outputMessages', null=True, to=orm['auth.User'])),
            ('dateCreate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(related_name='messages', null=True, to=orm['PManager.PM_Task'])),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['PManager.PM_Project'], null=True)),
            ('userTo', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='incomingMessages', null=True, to=orm['auth.User'])),
            ('hidden', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('hidden_from_clients', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('hidden_from_employee', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('isSystemLog', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('read', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('PManager', ['PM_Task_Message'])

        # Adding M2M table for field files on 'PM_Task_Message'
        m2m_table_name = db.shorten_name(u'PManager_pm_task_message_files')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pm_task_message', models.ForeignKey(orm['PManager.pm_task_message'], null=False)),
            ('pm_files', models.ForeignKey(orm['PManager.pm_files'], null=False))
        ))
        db.create_unique(m2m_table_name, ['pm_task_message_id', 'pm_files_id'])

        # Adding model 'PM_Role'
        db.create_table(u'PManager_pm_role', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('tracker', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['PManager.PM_Tracker'])),
        ))
        db.send_create_signal('PManager', ['PM_Role'])

        # Adding model 'PM_ProjectRoles'
        db.create_table(u'PManager_pm_projectroles', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='userRoles', to=orm['auth.User'])),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(related_name='projectRoles', to=orm['PManager.PM_Project'])),
            ('role', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['PManager.PM_Role'])),
            ('rate', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('payment_type', self.gf('django.db.models.fields.CharField')(default='real_time', max_length=100)),
        ))
        db.send_create_signal('PManager', ['PM_ProjectRoles'])

        # Adding model 'PM_User_PlanTime'
        db.create_table(u'PManager_pm_user_plantime', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['PManager.PM_Task'])),
            ('time', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal('PManager', ['PM_User_PlanTime'])

        # Adding model 'Specialty'
        db.create_table(u'PManager_specialty', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal('PManager', ['Specialty'])

        # Adding model 'PM_User'
        db.create_table(u'PManager_pm_user', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('icq', self.gf('django.db.models.fields.CharField')(max_length=70, null=True, blank=True)),
            ('skype', self.gf('django.db.models.fields.CharField')(max_length=70, null=True, blank=True)),
            ('birthday', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('avatar', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('sp_price', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('paid', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('specialty', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['PManager.Specialty'], null=True, blank=True)),
            ('avatar_color', self.gf('django.db.models.fields.CharField')(default='#00ee76', max_length=20, null=True, blank=True)),
            ('account_total', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('rating', self.gf('django.db.models.fields.FloatField')(default=0, null=True, blank=True)),
            ('last_activity_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('is_outsource', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('PManager', ['PM_User'])

        # Adding M2M table for field trackers on 'PM_User'
        m2m_table_name = db.shorten_name(u'PManager_pm_user_trackers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pm_user', models.ForeignKey(orm['PManager.pm_user'], null=False)),
            ('pm_tracker', models.ForeignKey(orm['PManager.pm_tracker'], null=False))
        ))
        db.create_unique(m2m_table_name, ['pm_user_id', 'pm_tracker_id'])

        # Adding M2M table for field specialties on 'PM_User'
        m2m_table_name = db.shorten_name(u'PManager_pm_user_specialties')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pm_user', models.ForeignKey(orm['PManager.pm_user'], null=False)),
            ('specialty', models.ForeignKey(orm['PManager.specialty'], null=False))
        ))
        db.create_unique(m2m_table_name, ['pm_user_id', 'specialty_id'])

        # Adding model 'PM_Achievement'
        db.create_table(u'PManager_pm_achievement', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('condition', self.gf('django.db.models.fields.TextField')()),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('PManager', ['PM_Achievement'])

        # Adding model 'PM_User_Achievement'
        db.create_table(u'PManager_pm_user_achievement', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_achievements', to=orm['auth.User'])),
            ('achievement', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['PManager.PM_Achievement'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('read', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('PManager', ['PM_User_Achievement'])

        # Adding model 'PM_Notice'
        db.create_table(u'PManager_pm_notice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('html', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('itemClass', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('PManager', ['PM_Notice'])

        # Adding model 'PM_NoticedUsers'
        db.create_table(u'PManager_pm_noticedusers', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='notices', to=orm['auth.User'])),
            ('notice', self.gf('django.db.models.fields.related.ForeignKey')(related_name='userNotices', to=orm['PManager.PM_Notice'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 11, 2, 0, 0))),
        ))
        db.send_create_signal('PManager', ['PM_NoticedUsers'])

        # Adding model 'Agent'
        db.create_table(u'PManager_agent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('seconds', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('method', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('required', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('once', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('last_result_message', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('last_process_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('PManager', ['Agent'])

        # Adding model 'LogData'
        db.create_table(u'PManager_logdata', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('value', self.gf('django.db.models.fields.IntegerField')()),
            ('project_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('PManager', ['LogData'])

        # Adding model 'Payment'
        db.create_table(u'PManager_payment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='payments', null=True, to=orm['auth.User'])),
            ('payer', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='repayments', null=True, to=orm['auth.User'])),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='payments', null=True, to=orm['PManager.PM_Project'])),
            ('value', self.gf('django.db.models.fields.IntegerField')()),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
        ))
        db.send_create_signal('PManager', ['Payment'])

        # Adding model 'Credit'
        db.create_table(u'PManager_credit', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='arrears', null=True, to=orm['auth.User'])),
            ('payer', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='credits', null=True, to=orm['auth.User'])),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='credits', null=True, to=orm['PManager.PM_Project'])),
            ('value', self.gf('django.db.models.fields.IntegerField')()),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='costs', null=True, to=orm['PManager.PM_Task'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
        ))
        db.send_create_signal('PManager', ['Credit'])

        # Adding model 'AccessInterface'
        db.create_table(u'PManager_accessinterface', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('port', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('protocol', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['PManager.PM_Project'])),
        ))
        db.send_create_signal('PManager', ['AccessInterface'])

        # Adding M2M table for field access_roles on 'AccessInterface'
        m2m_table_name = db.shorten_name(u'PManager_accessinterface_access_roles')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('accessinterface', models.ForeignKey(orm['PManager.accessinterface'], null=False)),
            ('pm_role', models.ForeignKey(orm['PManager.pm_role'], null=False))
        ))
        db.create_unique(m2m_table_name, ['accessinterface_id', 'pm_role_id'])

        # Adding model 'Key'
        db.create_table(u'PManager_key', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('file_path', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('key_data', self.gf('django.db.models.fields.TextField')()),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('PManager', ['Key'])


    def backwards(self, orm):
        # Deleting model 'Tags'
        db.delete_table(u'PManager_tags')

        # Deleting model 'ObjectTags'
        db.delete_table(u'PManager_objecttags')

        # Deleting model 'PM_Tracker'
        db.delete_table(u'PManager_pm_tracker')

        # Deleting model 'PM_Project'
        db.delete_table(u'PManager_pm_project')

        # Deleting model 'PM_File_Category'
        db.delete_table(u'PManager_pm_file_category')

        # Removing M2M table for field projects on 'PM_File_Category'
        db.delete_table(db.shorten_name(u'PManager_pm_file_category_projects'))

        # Deleting model 'PM_Files'
        db.delete_table(u'PManager_pm_files')

        # Removing M2M table for field versions on 'PM_Files'
        db.delete_table(db.shorten_name(u'PManager_pm_files_versions'))

        # Deleting model 'PM_Task_Status'
        db.delete_table(u'PManager_pm_task_status')

        # Deleting model 'PM_Milestone'
        db.delete_table(u'PManager_pm_milestone')

        # Removing M2M table for field responsible on 'PM_Milestone'
        db.delete_table(db.shorten_name(u'PManager_pm_milestone_responsible'))

        # Deleting model 'PM_Task'
        db.delete_table(u'PManager_pm_task')

        # Removing M2M table for field responsible on 'PM_Task'
        db.delete_table(db.shorten_name(u'PManager_pm_task_responsible'))

        # Removing M2M table for field observers on 'PM_Task'
        db.delete_table(db.shorten_name(u'PManager_pm_task_observers'))

        # Removing M2M table for field perhapsResponsible on 'PM_Task'
        db.delete_table(db.shorten_name(u'PManager_pm_task_perhapsResponsible'))

        # Removing M2M table for field viewedUsers on 'PM_Task'
        db.delete_table(db.shorten_name(u'PManager_pm_task_viewedUsers'))

        # Removing M2M table for field files on 'PM_Task'
        db.delete_table(db.shorten_name(u'PManager_pm_task_files'))

        # Deleting model 'PM_Timer'
        db.delete_table(u'PManager_pm_timer')

        # Deleting model 'PM_Properties'
        db.delete_table(u'PManager_pm_properties')

        # Deleting model 'PM_Property_Values'
        db.delete_table(u'PManager_pm_property_values')

        # Deleting model 'PM_Task_Message'
        db.delete_table(u'PManager_pm_task_message')

        # Removing M2M table for field files on 'PM_Task_Message'
        db.delete_table(db.shorten_name(u'PManager_pm_task_message_files'))

        # Deleting model 'PM_Role'
        db.delete_table(u'PManager_pm_role')

        # Deleting model 'PM_ProjectRoles'
        db.delete_table(u'PManager_pm_projectroles')

        # Deleting model 'PM_User_PlanTime'
        db.delete_table(u'PManager_pm_user_plantime')

        # Deleting model 'Specialty'
        db.delete_table(u'PManager_specialty')

        # Deleting model 'PM_User'
        db.delete_table(u'PManager_pm_user')

        # Removing M2M table for field trackers on 'PM_User'
        db.delete_table(db.shorten_name(u'PManager_pm_user_trackers'))

        # Removing M2M table for field specialties on 'PM_User'
        db.delete_table(db.shorten_name(u'PManager_pm_user_specialties'))

        # Deleting model 'PM_Achievement'
        db.delete_table(u'PManager_pm_achievement')

        # Deleting model 'PM_User_Achievement'
        db.delete_table(u'PManager_pm_user_achievement')

        # Deleting model 'PM_Notice'
        db.delete_table(u'PManager_pm_notice')

        # Deleting model 'PM_NoticedUsers'
        db.delete_table(u'PManager_pm_noticedusers')

        # Deleting model 'Agent'
        db.delete_table(u'PManager_agent')

        # Deleting model 'LogData'
        db.delete_table(u'PManager_logdata')

        # Deleting model 'Payment'
        db.delete_table(u'PManager_payment')

        # Deleting model 'Credit'
        db.delete_table(u'PManager_credit')

        # Deleting model 'AccessInterface'
        db.delete_table(u'PManager_accessinterface')

        # Removing M2M table for field access_roles on 'AccessInterface'
        db.delete_table(db.shorten_name(u'PManager_accessinterface_access_roles'))

        # Deleting model 'Key'
        db.delete_table(u'PManager_key')


    models = {
        'PManager.accessinterface': {
            'Meta': {'object_name': 'AccessInterface'},
            'access_roles': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'file_categories'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['PManager.PM_Role']"}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 11, 2, 0, 0)'}),
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
            'avatar_color': ('django.db.models.fields.CharField', [], {'default': "'#DCDCDC'", 'max_length': '20', 'null': 'True', 'blank': 'True'}),
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
            'achievement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['PManager.PM_Achievement']"}),
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