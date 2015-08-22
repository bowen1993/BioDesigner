from django.db import models
from design.models import parts

# Create your models here.

class compound(models.Model):
    compound_id = models.CharField(primary_key=True, max_length=32)
    name = models.CharField(max_length=255, null=True)
    nicknames = models.TextField(null=True)
    formula = models.CharField(max_length=255)
    exact_mass = models.FloatField(null=True)
    mol_mass = models.FloatField(null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'bio_compound' 

class gene(models.Model):
    gene_id = models.CharField(primary_key=True, max_length=32)
    name = models.CharField(max_length=64)
    nicknames = models.TextField(null=True)
    definition = models.TextField(null=True)
    organism_short = models.CharField(max_length=16)
    organism = models.CharField(max_length=256)
    position = models.CharField(max_length=16)
    ntseq_length = models.IntegerField()
    ntseq = models.TextField(null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'bio_gene' 

class reaction(models.Model):
    reaction_id = models.CharField(primary_key=True, max_length=32)
    name = models.CharField(max_length=255)
    definition = models.TextField(null=True)
    equation = models.TextField(null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'bio_reactions' 

class reaction_compound(models.Model):
    reaction = models.ForeignKey(reaction)
    compound = models.ForeignKey(compound)
    isReactant = models.BooleanField(default=False)
    isResultant = models.BooleanField(default=False)
    amount = models.IntegerField(null=True, default=1)

    def __unicode__(self):
        return self.reaction_id

    class Meta:
        db_table = 'bio_reaction_compounds' 

class part_gene(models.Model):
    part = models.ForeignKey(parts)
    gene = models.ForeignKey(gene)
    score = models.FloatField()

    def __unicode__(self):
        return self.score

    class Meta:
        db_table = 'bio_part_gene'