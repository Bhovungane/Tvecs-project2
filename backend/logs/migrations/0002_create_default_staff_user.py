from django.db import migrations
from django.contrib.auth.models import User

def create_default_staff_user(apps, schema_editor):
    username = 'staff'
    password = 'staff'
    if not User.objects.filter(username=username).exists():
        User.objects.create_user(username=username, password=password, is_staff=True, is_active=True)
    else:
        user = User.objects.get(username=username)
        user.set_password(password)
        user.is_staff = True
        user.is_active = True
        user.save()

class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_staff_user),
    ]
