from django.db import models
from accounts.models import User

# Create your models here.
# 

class parts(models.Model):
    part_id          = models.IntegerField(primary_key=True)
    ok               = models.BooleanField(default=True)
    part_name        = models.CharField(max_length=255)
    short_desc       = models.CharField(max_length=255,null=True)
    description      = models.TextField(null=True)
    part_type        = models.CharField(max_length=20,null=True)
    author           = models.CharField(max_length=200,null=True)
    status           = models.CharField(max_length=20,null=True)
    dominant         = models.BooleanField(default=True)
    discontinued     = models.IntegerField(null=True)
    part_status      = models.CharField(max_length=40,null=True)
    sample_status    = models.CharField(max_length=40,null=True)
    p_status_cache   = models.CharField(max_length=1000,null=True)
    s_status_cache   = models.CharField(max_length=1000,null=True)
    in_stock         = models.BooleanField(default=True)
    results          = models.CharField(max_length=20, null=True)
    favorite         = models.IntegerField(null=True)
    specified_u_list = models.TextField(null=True)
    deep_u_list      = models.TextField(null=True)
    deep_count       = models.IntegerField(null=True)
    ps_string        = models.TextField(null=True)
    scars            = models.CharField(max_length=20,null=True)
    barcode          = models.CharField(max_length=50,null=True)
    notes            = models.TextField(null=True)
    source           = models.TextField(null=True)
    nickname         = models.CharField(max_length=50,null=True)
    premium          = models.IntegerField(null=True)
    categories       = models.CharField(max_length=500,null=True)
    sequence         = models.TextField(null=True)
    sequence_length  = models.IntegerField(null=True)
    part_url = models.CharField(max_length=255, null=True)

    def __unicode__(self):
        return self.part_name

    class Meta:
        db_table = 'bio_parts' 

class part_parameters(models.Model):
    part = models.ForeignKey(parts)
    name = models.CharField(max_length=256)
    value = models.CharField(max_length=256)

    class Meta:
        db_table = 'bio_part_parameters'

class part_twins(models.Model):
    part_1 = models.ForeignKey(parts)
    part_2 = models.ForeignKey(parts, related_name='FK_PART_TWIN2', db_column='part_2_id')

    class Meta:
        db_table = 'bio_part_twins'

class features(models.Model):
    feature_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=128, null=True)
    feature_type = models.CharField(max_length=128, null=True)
    direction = models.CharField(max_length=256, null=True)
    startpos = models.IntegerField(null=True)
    endpos = models.IntegerField(null=True)
    
    class Meta:
        db_table = 'bio_features'

class part_features(models.Model):
    part = models.ForeignKey(parts)
    feature = models.ForeignKey(features)

    class Meta:
        db_table = 'bio_part_features'


class tracks(models.Model):
    track    = models.CharField(max_length=64)

    def __unicode__(self):
        return self.track

    class Meta:
        db_table = 'bio_tracks'

class functions(models.Model):
    function = models.CharField(max_length=255, null=True)

    def __unicode__(self):
        return self.function

    class Meta:
        db_table = 'bio_functions'

class track_functions(models.Model):
    track = models.ForeignKey(tracks)
    function = models.ForeignKey(functions)

    def __unicode__(self):
        return '%s %s' % (self.track, self.function)

    class Meta:
        db_table = 'bio_track_function'

class teams(models.Model):
    team_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=64)
    track = models.ForeignKey(tracks)
    function = models.ForeignKey(functions)
    year = models.CharField(max_length=16)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'bio_team'

class project(models.Model):
    project_name = models.CharField(max_length=64)
    creator      = models.ForeignKey(User)
    create_time  = models.DateTimeField(auto_now_add=True)
    function     = models.ForeignKey(functions, null=True)
    track        = models.ForeignKey(tracks, null=True)
    is_deleted   = models.BooleanField(default=False)

    def __unicode__(self):
        return self.project_name

    class Meta:
        db_table = 'bio_project'

class team_parts(models.Model):
    team   = models.ForeignKey(teams)
    part = models.ForeignKey(parts)

    def __unicode__(self):
        return self.team_name

    class Meta:
        db_table = 'bio_team_parts'


class user_project(models.Model):
    user    = models.ForeignKey(User)
    project = models.ForeignKey(project)

    def __unicode__(self):
        return self.user

    class Meta:
        db_table = 'bio_user_project'

class chain(models.Model):
    sequence = models.CharField(max_length=255,null=True)
    project  = models.ForeignKey(project)
    name = models.CharField(max_length=64, null=False)
    isModified = models.BooleanField(default=True)
    image_file_path = models.CharField(max_length=255, null=True)
    def __unicode__(self):
        return self.sequence

    class Meta:
        db_table = 'bio_chain'


