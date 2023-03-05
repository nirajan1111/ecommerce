from django.db import migrations
from api.user.models import CustomUser


class Migration(migrations.Migration):
    def seed_data(apps, schema_editor):
        user = CustomUser(name="nirajan", email="nirajan@gmail.com",
                          is_staff=True, is_superuser=True, phone="9829004337", gender="Male")
        user.set_password("12345")
        user.save()
        dependencies = [
            ('auth', '0011_update_proxy_permissions'),
        ]
    operations = [
        migrations.RunPython(seed_data),
    ]
