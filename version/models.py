from django.db import models
from design.models import project
from accounts.models import User
import datetime

# Create your models here.
class version(models.Model):
    version_id          = models.CharField(max_length=64,primary_key=True)
    project             = models.ForeignKey(project)
    modifyTime          = models.DateTimeField(auto_now=True)
    modifyPerson        = models.ForeignKey(User)
    version_description = models.TextField()
    # content is consists of chains and chains are seperated by char ','
    content             = models.TextField()

    def __unicode__(self):
        return self.version_id

    class Meta:
        db_table = 'bio_version'