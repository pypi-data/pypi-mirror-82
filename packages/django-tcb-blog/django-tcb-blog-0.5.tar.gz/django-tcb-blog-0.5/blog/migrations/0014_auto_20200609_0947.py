# Generated by Django 3.0.3 on 2020-06-09 09:47

from django.db import migrations


def populate_version_publish_publish_date(apps, schema_editor):
    EntryEnvelope = apps.get_model('blog', 'EntryEnvelope')
    ees = EntryEnvelope.objects.all()

    for ee in ees:
        if ee.published:
            ee.entry['published'] = True
        else:
            ee.entry['published'] = False
        if ee.publish_date is not None:
            ee.entry['publish_date'] = ee.publish_date.isoformat()
        if ee.version:
            ee.entry['version'] = ee.version
        else:
            ee.entry['version'] = 1
        ee.save()


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_entryenvelope_version'),
    ]

    operations = [
        migrations.RunPython(populate_version_publish_publish_date,
                             reverse_code=migrations.RunPython.noop)
    ]
