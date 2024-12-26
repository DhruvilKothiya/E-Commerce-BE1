# Generated by Django 5.1.4 on 2024-12-26 08:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='products',
            name='_id',
        ),
        migrations.RemoveField(
            model_name='products',
            name='numReviews',
        ),
        migrations.RemoveField(
            model_name='products',
            name='productcategory',
        ),
        migrations.AddField(
            model_name='products',
            name='id',
            field=models.BigAutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='products',
            name='size',
            field=models.CharField(blank=True, default=0, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='products',
            name='rating',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True),
        ),
        migrations.AddField(
            model_name='products',
            name='category',
            field=models.ForeignKey(blank=True, default='a', null=True, on_delete=django.db.models.deletion.SET_NULL, to='ecomapp.categories'),
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecomapp.products')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]