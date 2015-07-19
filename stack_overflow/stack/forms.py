from __future__ import unicode_literals
from .models import Profile, Answers, Tag, Question
from django import forms
from django.forms.models import inlineformset_factory



class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['email']

class AnswerForm(forms.ModelForm):

    class Meta:
        model = Answers
        fields = ['text']

class TagForm(forms.ModelForm):

    class Meta:
        model = Tag
        fields = ['tag']










# class ProfileEditForm(forms.ModelForm):

   # class Meta:
       # model = Profile

        # fields = ['customer', 'staff', 'owner']