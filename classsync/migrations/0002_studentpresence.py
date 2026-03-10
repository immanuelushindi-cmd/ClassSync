from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('classsync', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentPresence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voter_key', models.CharField(max_length=64)),
                ('last_seen', models.DateTimeField(auto_now=True)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='presences', to='classsync.session')),
            ],
            options={
                'unique_together': {('session', 'voter_key')},
            },
        ),
    ]
