# Generated by Django 5.1.1 on 2024-09-18 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="MasterBank",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "bank_code",
                    models.CharField(
                        max_length=50, unique=True, verbose_name="은행 코드"
                    ),
                ),
                ("bank_name", models.CharField(max_length=100, verbose_name="은행명")),
            ],
            options={
                "verbose_name": "은행 정보",
                "verbose_name_plural": "은행 정보들",
            },
        ),
    ]
