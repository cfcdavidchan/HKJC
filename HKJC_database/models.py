from django.db import models

# Create your models here.
class Going(models.Model):
    track = models.CharField(max_length= 50,
                             blank= False,
                             help_text='Enter the type of track')

    condition = models.CharField(max_length= 50,
                             blank= False,
                             help_text='Enter the condition')

    chinese_condition = models.CharField(max_length= 50,
                             blank= True,
                             help_text='Enter the chinese condition')

    code = models.CharField(max_length= 5,
                             blank= False,
                             help_text='Enter the condition code')

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.name

    class Meta:
        ordering = ['track']

class RacingCourse(models.Model):
    place = models.CharField(max_length= 50,
                             blank= False,
                             help_text='Enter the place of track')

    chinese_place = models.CharField(max_length= 50,
                             blank= True,
                             help_text='Enter the Chinese place name of the track')

    course = models.CharField(max_length= 5,
                             blank= True,
                             help_text='Enter the course of the track')

    home_straight_M = models.PositiveIntegerField(blank= True,
                                                  help_text='Enter the condition code')

    width_M = models.DecimalField(max_digits=10,
                                  decimal_places=10)
    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.name

    class Meta:
        ordering = ['course']

class Jockey(models.Model):
    name = models.CharField(max_length=50,
                             blank=False,
                             help_text="Enter the jockey's name")

    chinese_name = models.CharField(max_length=50,
                                     blank=True,
                                     help_text="Enter the jockey's chinese name")

    hkjc_id = models.CharField(max_length= 10,
                             blank= False,
                             help_text="Enter the jockey's hkjc id")

