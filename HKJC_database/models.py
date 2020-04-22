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

    home_straight_M = models.FloatField(help_text= 'Enter the Home Straight(M)'
                                        )

    width_M = models.FloatField(help_text= 'Enter the Width(M)'
                                )

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.name

    class Meta:
        ordering = ['course']

class Jockey_Info(models.Model):
    name = models.CharField(max_length=50,
                             blank=False,
                             help_text="Enter the jockey's name")

    chinese_name = models.CharField(max_length=50,
                                     blank=True,
                                     help_text="Enter the jockey's chinese name")

    hkjc_id = models.CharField(max_length= 10,
                             blank= False,
                             help_text="Enter the jockey's hkjc id")
    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.name

    class Meta:
        ordering = ['name']

class Jockey_Report(models.Model):
    jockey = models.ForeignKey(Jockey_Info,
                               related_name= 'Jockey_Info',
                               on_delete= models.SET_NULL,
                               null= True
                               )

    stakes_won = models.FloatField(help_text= 'Enter the stakes Stakes won'
                                )

    wins_past_10_racing = models.PositiveSmallIntegerField(help_text= 'Enter the No. of Wins in past 10 race days'
                                )

    avg_JKC_past_10 = models.FloatField(help_text= 'Avg. JKC points in Past 10 race days'
                                )

    number_win = models.IntegerField(help_text= 'No. of Wins'
                                     )

    number_second = models.IntegerField(help_text= 'No. of 2nds'
                                     )

    number_third = models.IntegerField(help_text= 'No. of 3rds'
                                     )

    number_fourth = models.IntegerField(help_text= 'No. of 4ths'
                                     )

    total_rides = models.IntegerField(help_text= 'Total Rides'
                                     )

    win_rate = models.FloatField(help_text= 'Win %'
                                )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['number_win']

class Trainer_Info(models.Model):
    name = models.CharField(max_length=50,
                             blank=False,
                             help_text="Enter the Trainer's name")

    chinese_name = models.CharField(max_length=50,
                                     blank=True,
                                     help_text="Enter the Trainer's chinese name")

    hkjc_id = models.CharField(max_length= 10,
                             blank= False,
                             help_text="Enter the jockey's hkjc id")

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.name

    class Meta:
        ordering = ['name']


class Trainer_Report(models.Model):
    trainer = models.ForeignKey(Trainer_Info,
                               related_name= 'Trainer_Info',
                               on_delete= models.SET_NULL,
                               null= True
                               )

    stakes_won = models.FloatField(help_text= 'Enter the stakes Stakes won'
                                )

    wins_past_10_racing = models.PositiveSmallIntegerField(help_text= 'Enter the No. of Wins in past 10 race days'
                                )

    number_win = models.IntegerField(help_text= 'No. of Wins'
                                     )

    number_second = models.IntegerField(help_text= 'No. of 2nds'
                                     )

    number_third = models.IntegerField(help_text= 'No. of 3rds'
                                     )

    number_fourth = models.IntegerField(help_text= 'No. of 4ths'
                                     )

    total_runners = models.IntegerField(help_text= 'Total Runners'
                                     )

    win_rate = models.FloatField(help_text= 'Win %'
                                )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['number_win']