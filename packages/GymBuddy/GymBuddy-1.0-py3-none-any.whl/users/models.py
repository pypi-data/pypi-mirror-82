from django.db import models
from django.contrib.auth.models import User
from activityLibrary.models import Exercise
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(default='default.jpg', upload_to='profile_pics')
    goal_weight_change = models.IntegerField(default=0)
    activity_level = models.DecimalField(max_digits=2, decimal_places=1, default=1.5)
    current_weight = models.IntegerField(help_text='Enter in lbs', default = 100)
    carb_percent = models.DecimalField(help_text='Recommended carbohydrate intake is between 45-65% of caloric intake',max_digits=3,decimal_places=1, default=55)
    fat_percent = models.DecimalField(help_text='Recommended fat intake is between 20-25% of caloric intake',max_digits=3,decimal_places=1,default=25)
    protein_percent = models.DecimalField(help_text='Recommended protein intake is between 80-100% of current body weight',max_digits=3,decimal_places=1, default=20)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    daily_cal_in = models.IntegerField()
    daily_carbs = models.IntegerField()
    daily_fat = models.IntegerField()
    daily_protein = models.IntegerField()

    def __str__(self):
        return f'{self.user.username} Profile'



class WeightRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lbs = models.IntegerField()
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username}: {self.lbs} on {self.date}"

class LiftRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets = models.IntegerField(blank=True, null=True)
    reps_per_set = models.IntegerField(blank=True, null=True)
    date = models.DateField()

class LiftRecord2(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    weight = models.IntegerField(blank=True, null=True)
    sets = models.IntegerField(blank=True, null=True)
    reps = models.IntegerField(blank=True, null=True)
    date = models.DateField(default=timezone.now)



