# Generated by Django 4.1.5 on 2023-01-24 09:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Hotel_managements', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id_reservation', models.AutoField(primary_key=True, serialize=False)),
                ('user_update', models.CharField(max_length=100)),
                ('room_type', models.CharField(max_length=100)),
                ('Quantity', models.IntegerField()),
                ('checkin_date', models.DateField()),
                ('checkin_time', models.TimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='Hotel_managements.hotel')),
            ],
            options={
                'db_table': 'reservation',
            },
        ),
    ]
