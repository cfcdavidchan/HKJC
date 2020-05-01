from django.contrib import admin
from .models import Going, RacingCourse, Jockey_Info, Jockey_Report, Trainer_Info , Trainer_Report, Horse_Info, Horse_Report, Horse_Ranking, Match_Info, Match_Result
# Register your models here.
@admin.register(Going)
class GoingAdmin(admin.ModelAdmin):
    list_display = ('track', 'condition','chinese_condition')
    pass

@admin.register(RacingCourse)
class RacingCourseAdmin(admin.ModelAdmin):
    list_display = ('place', 'chinese_place','course')
    pass

@admin.register(Jockey_Info)
class Jockey_InfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'chinese_name','hkjc_id')
    pass

@admin.register(Jockey_Report)
class Jockey_ReportAdmin(admin.ModelAdmin):
    list_display = ('jockey', 'season','number_win', 'total_rides', 'win_rate')
    pass

@admin.register(Trainer_Info)
class Trainer_InfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'chinese_name','hkjc_id')
    pass

@admin.register(Trainer_Report)
class Trainer_ReportAdmin(admin.ModelAdmin):
    list_display = ('trainer', 'stakes_won','number_win', 'win_rate')
    pass

@admin.register(Horse_Info)
class Horse_InfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'chinese_name','hkjc_id', 'trainer')
    pass

@admin.register(Horse_Report)
class Horse_ReportAdmin(admin.ModelAdmin):
    list_display = ('horse', 'current_rank','total_stakes')
    pass

@admin.register(Horse_Ranking)
class Horse_RankingAdmin(admin.ModelAdmin):
    list_display = ('horse', 'rank','rank_reord_date')
    pass

@admin.register(Match_Info)
class Match_InfoAdmin(admin.ModelAdmin):
    list_display = ('match_date', 'match_place','race_number','match_class','distance_M')
    pass

@admin.register(Match_Result)
class Match_ResultAdmin(admin.ModelAdmin):
    list_display = ('match', 'horse_place','horse_no','horse','jockey','draw','finish_time')
    pass