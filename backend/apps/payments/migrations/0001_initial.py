from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan', models.CharField(choices=[('FREE', 'Free'), ('BASIC', 'Basic'), ('PREMIUM', 'Premium'), ('CONSULTANT_PRO', 'Consultant Pro'), ('SCHOOL_PARTNER', 'School Partner'), ('EMPLOYER_PARTNER', 'Employer Partner'), ('ENTERPRISE', 'Enterprise')], default='FREE', max_length=40)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('provider', models.CharField(max_length=30)),
                ('reference', models.CharField(max_length=120, unique=True)),
                ('status', models.CharField(default='pending', max_length=30)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan', models.CharField(choices=[('FREE', 'Free'), ('BASIC', 'Basic'), ('PREMIUM', 'Premium'), ('CONSULTANT_PRO', 'Consultant Pro'), ('SCHOOL_PARTNER', 'School Partner'), ('EMPLOYER_PARTNER', 'Employer Partner'), ('ENTERPRISE', 'Enterprise')], default='FREE', max_length=40)),
                ('active', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
