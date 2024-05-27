from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Course
User = get_user_model()

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class CourseSearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'profile_picture']

class CourseCompletionForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    courses = forms.ModelMultipleChoiceField(queryset=Course.objects.all(), widget=forms.CheckboxSelectMultiple)

