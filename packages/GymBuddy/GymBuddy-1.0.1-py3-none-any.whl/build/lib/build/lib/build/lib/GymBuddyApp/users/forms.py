from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from .models import WeightRecord
from .models import LiftRecord2
from .models import Food

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        #we probably want to change the labels of the fields on the front end
        #example: daily_cal_in = forms.IntegerField(label="Daily Calories")
        fields = ['daily_cal_in', 'daily_carbs', 'daily_fat', 'daily_protein','starting_weight', 'goal_weight_change','activity_level']

class WeightForm(forms.ModelForm):
    class Meta:
        model = WeightRecord
        fields = ['lbs', 'date']

class Lift2Form(forms.ModelForm):
    class Meta:
        model = LiftRecord2
        fields = ['name','weight', 'sets', 'reps', 'date']

class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ['name','carbs', 'fats', 'protein', 'date']

class OptionForm(forms.Form):
    optionName = forms.ChoiceField()
