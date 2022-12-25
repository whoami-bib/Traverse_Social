from django import forms

from .models import Tweet

MAX_TWEET_LENGTH = 240
class TweetForm(forms.ModelForm):
    """
    this is a form for creating a post
    def clean_data is a function for validating the input before submitting 
    """
    
    class Meta:
        model  = Tweet
        fields = ['content']

    def clean_content(self):
        content = self.cleaned_data.get("content")
        if len(content) > MAX_TWEET_LENGTH:
            raise forms.ValidationError("This Traverse is Too long")
        return content
