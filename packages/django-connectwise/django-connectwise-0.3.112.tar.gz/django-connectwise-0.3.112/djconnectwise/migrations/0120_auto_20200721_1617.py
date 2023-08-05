# Generated by Django 2.1.14 on 2020-07-21 16:17

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('djconnectwise', '0119_auto_20200624_1028'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectTeamMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('member', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='djconnectwise.Member')),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='djconnectwise.Project')),
                ('work_role', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='djconnectwise.WorkRole')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='project',
            name='team_members',
            field=models.ManyToManyField(through='djconnectwise.ProjectTeamMember', to='djconnectwise.Member'),
        ),
    ]
