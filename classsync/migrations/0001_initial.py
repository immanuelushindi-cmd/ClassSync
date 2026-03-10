from django.db import migrations, models
import django.db.models.deletion
import classsync.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('subject', models.CharField(max_length=100)),
                ('pin', models.CharField(default=classsync.models.generate_pin, max_length=4, unique=True)),
                ('teacher_name', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Doubt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=500)),
                ('topic_tag', models.CharField(blank=True, default='', max_length=80)),
                ('votes', models.IntegerField(default=0)),
                ('is_answered', models.BooleanField(default=False)),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doubts', to='classsync.session')),
            ],
            options={
                'ordering': ['-votes', '-submitted_at'],
            },
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voter_key', models.CharField(max_length=64)),
                ('doubt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vote_records', to='classsync.doubt')),
            ],
            options={
                'unique_together': {('doubt', 'voter_key')},
            },
        ),
    ]
