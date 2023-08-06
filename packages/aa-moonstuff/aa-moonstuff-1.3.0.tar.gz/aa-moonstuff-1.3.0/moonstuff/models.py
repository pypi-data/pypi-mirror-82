from django.db import models
from allianceauth.eveonline.models import EveCorporationInfo, EveCharacter


# Create your models here.
class Ore(models.Model):
    group_id = models.IntegerField()
    group_name = models.CharField(max_length=255)
    ore_name = models.CharField(max_length=75)
    ore_id = models.IntegerField(primary_key=True)
    unit_value = models.FloatField(null=True)
    volume = models.FloatField(null=True)

    def __str__(self):
        return "{} - {}".format(self.group_name, self.ore_name)


class Resource(models.Model):
    ore = models.CharField(max_length=75)
    ore_id = models.ForeignKey(Ore, on_delete=models.DO_NOTHING)
    amount = models.DecimalField(max_digits=11, decimal_places=10)

    def __str__(self):
        return "{} - {}".format(self.ore, self.amount)

    class Meta:
        unique_together = (('amount', 'ore_id'),)


class Moon(models.Model):
    name = models.CharField(max_length=80)
    system_id = models.IntegerField()
    moon_id = models.IntegerField()
    resources = models.ManyToManyField(Resource)

    def __str__(self):
        return self.name

    class Meta:
        permissions = (
            ('view_moonstuff', 'Can access the moonstuff module.'),
        )


def get_fallback_moon():
    return Moon.objects.get_or_create(system_id=30000142, moon_id=40009087)


class Refinery(models.Model):
    name = models.CharField(max_length=150)
    structure_id = models.CharField(max_length=15)
    size = models.BooleanField()
    location = models.ForeignKey(Moon, on_delete=models.SET(get_fallback_moon))
    owner = models.ForeignKey(EveCorporationInfo, on_delete=models.CASCADE)

    @property
    def size_to_string(self):
        if self.size is True:
            return "Large"
        else:
            return "Medium"

    def __str__(self):
        return self.name


class ExtractEvent(models.Model):
    start_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    decay_time = models.DateTimeField()
    structure = models.ForeignKey(Refinery, on_delete=models.CASCADE)
    moon = models.ForeignKey(Moon, on_delete=models.CASCADE)
    corp = models.ForeignKey(EveCorporationInfo, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('arrival_time', 'moon'),)

    def __str__(self):
        return "{} - {}".format(self.moon.name, self.arrival_time)


class MoonDataCharacter(models.Model):
    character = models.OneToOneField(EveCharacter, on_delete=models.CASCADE)
    latest_notification = models.BigIntegerField(null=True, default=0)
