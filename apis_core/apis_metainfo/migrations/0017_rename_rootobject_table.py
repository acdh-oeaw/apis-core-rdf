from django.db import migrations


class Migration(migrations.Migration):
    atomic = False
    dependencies = [
        ('apis_metainfo', '0016_remove_rootobject_self_contenttype'),
    ]
    state_operations = [
        migrations.DeleteModel(
            name='RootObject',
        ),
    ]
    operations = [
        migrations.AlterModelTable(
            name='RootObject',
            table='entities_entity'
        ),
        migrations.SeparateDatabaseAndState(
            database_operations=None,
            state_operations=state_operations
        )
    ]
