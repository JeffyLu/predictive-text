# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-13 23:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predictive', '0002_delete_vocabularyrelation'),
    ]

    operations = [
        migrations.CreateModel(
            name='VocabularyRelation_0',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vocab_id', models.BigIntegerField(db_index=True)),
                ('next_vocab_id', models.BigIntegerField()),
                ('frequency', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'predictive_vocabularyrelation_0',
            },
        ),
        migrations.CreateModel(
            name='VocabularyRelation_1',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vocab_id', models.BigIntegerField(db_index=True)),
                ('next_vocab_id', models.BigIntegerField()),
                ('frequency', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'predictive_vocabularyrelation_1',
            },
        ),
        migrations.CreateModel(
            name='VocabularyRelation_2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vocab_id', models.BigIntegerField(db_index=True)),
                ('next_vocab_id', models.BigIntegerField()),
                ('frequency', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'predictive_vocabularyrelation_2',
            },
        ),
        migrations.CreateModel(
            name='VocabularyRelation_3',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vocab_id', models.BigIntegerField(db_index=True)),
                ('next_vocab_id', models.BigIntegerField()),
                ('frequency', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'predictive_vocabularyrelation_3',
            },
        ),
        migrations.AlterUniqueTogether(
            name='vocabularyrelation_3',
            unique_together=set([('vocab_id', 'next_vocab_id')]),
        ),
        migrations.AlterUniqueTogether(
            name='vocabularyrelation_2',
            unique_together=set([('vocab_id', 'next_vocab_id')]),
        ),
        migrations.AlterUniqueTogether(
            name='vocabularyrelation_1',
            unique_together=set([('vocab_id', 'next_vocab_id')]),
        ),
        migrations.AlterUniqueTogether(
            name='vocabularyrelation_0',
            unique_together=set([('vocab_id', 'next_vocab_id')]),
        ),
    ]
