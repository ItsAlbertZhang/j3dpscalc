from django.db import models

# Create your models here.

class GlobalParam(models.Model):
    level_min = models.IntegerField()
    level_max = models.IntegerField()
    level_coefficient = models.IntegerField()
    level_constant = models.IntegerField()
    Hit = models.FloatField()
    CriticalStrike = models.FloatField()
    CriticalDamagePower = models.FloatField()
    Strain = models.FloatField()
    Surplus = models.FloatField()
    Overcome = models.FloatField()
    Haste = models.FloatField()
    Shield = models.FloatField()
    Dodge = models.FloatField()
    Parry = models.FloatField()
    Toughness = models.FloatField()
    DecriticalDamagePower = models.FloatField()

    def __str__(self) -> str:
        return f'{self.level_min}, {self.level_max}, {self.level_coefficient}, {self.level_constant}\n'

    class Meta:
        db_table = 'global_param'
