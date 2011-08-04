from django.db import models

# Create your models here.
class Setting(models.Model):
    tag = models.CharField('Tag Name', max_length = 15, primary_key=True)
    value = models.CharField('Tag Value', max_length = 50)
    description = models.TextField('Tag Description', blank=True)

    def __unicode__(self):
        return "%s - %s" %(self.tag, self.value)
