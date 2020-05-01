from django.db import models
from django.contrib.postgres.fields import JSONField

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

    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.track

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

    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.place

    class Meta:
        ordering = ['place']

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

    modified_date = models.DateTimeField(auto_now=True)
    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.name

    class Meta:
        ordering = ['name']

class Jockey_Report(models.Model):
    jockey = models.ForeignKey(Jockey_Info,
                               related_name= 'jockey_Info_jockey',
                               on_delete= models.SET_NULL,
                               null= True
                               )

    season = models.CharField(max_length= 30,
                              help_text="Enter the seaon of this record"
                              )

    stakes_won = models.FloatField(help_text= 'Enter the stakes Stakes won'
                                   )

    wins_past_10_racing = models.PositiveSmallIntegerField(help_text= 'Enter the No. of Wins in past 10 race days',
                                                           blank=True)

    avg_JKC_past_10 = models.FloatField(help_text= 'Avg. JKC points in Past 10 race days',
                                        blank=True)

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

    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-season','-number_win',]

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

    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.name

    class Meta:
        ordering = ['name']

class Trainer_Report(models.Model):
    trainer = models.ForeignKey(Trainer_Info,
                               related_name= 'trainer_report_Trainer',
                               on_delete= models.SET_NULL,
                               null= True
                               )

    season = models.CharField(max_length= 30,
                              help_text="Enter the seaon of this record"
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

    win_stat = JSONField(help_text= 'Enter the json of the win state'
                                )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['number_win']

class Horse_Info(models.Model):
    name = models.CharField(max_length=50,
                             blank=False,
                             help_text="Enter the horse's name")

    chinese_name = models.CharField(max_length=50,
                                     blank=True,
                                     help_text="Enter the horse's chinese name")

    hkjc_id = models.CharField(max_length= 20,
                             blank= False,
                             help_text="Enter the horse's hkjc id")

    origin = models.CharField(max_length= 50,
                             blank= False,
                             help_text="Enter the horse's origin")

    age = models.IntegerField(help_text= "Enter the horse's age"
                              )

    trainer = models.ForeignKey(Trainer_Info,
                               related_name= 'horse_info_trainer',
                               on_delete= models.SET_NULL,
                               null= True
                               )

    owner = models.CharField(max_length= 100,
                             blank= False,
                             help_text="Enter the horse's owner")

    sire = models.CharField(max_length= 100,
                             blank= False,
                             help_text="Enter the horse's sire")

    dam = models.CharField(max_length= 100,
                             blank= False,
                             help_text="Enter the horse's dam")

    dam_sire = models.CharField(max_length= 100,
                                           blank= True,
                                           help_text="Enter the horse's dam_sire"
                                )

    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.name

    class Meta:
        ordering = ['name']

class Horse_Report(models.Model):
    horse = models.ForeignKey('Horse_info',
                               related_name= 'horse_info_horse',
                               on_delete= models.SET_NULL,
                               null= True
                               )

    current_rank = models.IntegerField(help_text="Enter the horse's current_rank"
                                       )

    season_start_rank = models.IntegerField(help_text="Enter the horse's starting rank of this season"
                                            )

    season_stakes = models.FloatField(help_text="Enter the horse's season stakes"
                                      )

    total_stakes = models.FloatField(help_text= "Enter the horse's total stakes"
                              )

    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['horse']

class Horse_Ranking(models.Model):
    horse = models.ForeignKey(Horse_Info,
                               related_name= 'horse_ranking_horse',
                               on_delete= models.SET_NULL,
                               null= True
                               )

    rank = models.IntegerField(help_text="Enter the horse's rank"
                               )

    rank_reord_date = models.DateField(help_text="Enter the record date of the rank"
                                       )
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['horse','rank','-rank_reord_date']

class Match_Info(models.Model):
    match_date = models.DateField(help_text="Enter the Match Date"
                                  )

    match_place = models.CharField(max_length= 50,
                                   help_text= 'Enter the place of the match'
                                   )

    race_number = models.IntegerField(help_text="Enter the race number"
                                      )

    distance_M = models.IntegerField(help_text="Enter the match distance (M)"
                                     )

    match_class = models.CharField(max_length= 100,
                                   help_text= "Enter the match class"
                                   )

    match_name = models.CharField(max_length= 200,
                                  help_text= "Enter the match name"
                                  )

    match_prize = models.FloatField(help_text="Enter the match prize"
                                    )

    match_going = models.CharField(max_length= 200,
                                   help_text= 'Enter the going of the match'
                                   )
    match_course = models.CharField(max_length= 200,
                                    help_text= 'Enter the course of the match'
                                    )

    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-match_date', 'race_number']

    # def __str__(self):
    #     """String for representing the MyModelName object (in Admin site etc.)."""
    #     from datetime import datetime
    #     date_string = datetime.strftime(self.match_date, '%Y/%m/%d')
    #     return date_string

class Match_Result(models.Model):
    match = models.ForeignKey(Match_Info,
                              related_name= 'match',
                              on_delete= models.SET_NULL,
                              null= True
                              )

    horse_place = models.CharField(max_length= 100,
                                   help_text= "Enter the horse place"
                                   )

    horse_no = models.IntegerField(help_text="Enter the horse number",
                                   blank=True,
                                   null=True
                                   )

    horse = models.ForeignKey(Horse_Info,
                              related_name= 'match_horse',
                              on_delete= models.SET_NULL,
                              null= True
                              )

    jockey = models.ForeignKey(Jockey_Info,
                              related_name= 'match_horse',
                              on_delete= models.SET_NULL,
                              null= True
                              )

    actual_weight = models.IntegerField(help_text="Enter actual weight of the horse",
                                        blank=True,
                                        null=True
                                        )

    declar_weight = models.IntegerField(help_text="Enter actual weight of the horse",
                                        blank=True,
                                        null=True
                                        )

    draw = models.IntegerField(help_text="Enter draw of the horse",
                               )

    finish_time = models.CharField(max_length= 200,
                                   help_text= "Enter the finish time"
                                   )

    win_odds = models.FloatField(help_text="Enter the win odds"
                                 )

    created_date = models.DateTimeField(auto_now_add=True)

