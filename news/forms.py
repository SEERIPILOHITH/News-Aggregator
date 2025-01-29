from .models import UserProfile,Bookmark,Article
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django import forms
from .models import UserProfile


class preference(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['topics']
        labels = {
            "topics": 'Topic of Interest'
        }
        widgets = {
            "topics": forms.TextInput(attrs={
                'placeholder': 'Enter topics (comma-separated)'
            })
        }

    def clean_topics(self):
        topics = self.cleaned_data.get('topics')
        topic_list = topics.split(",")
        if len(topic_list) > 5:
            raise forms.ValidationError("Only 5 topics are allowed.")
        return topics

class customUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ["username","email","password1","password2"]

