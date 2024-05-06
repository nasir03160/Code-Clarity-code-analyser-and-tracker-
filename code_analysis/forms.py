from django import forms
from .models import CodeSnippet

class CodeSnippetForm(forms.ModelForm):
    class Meta:
        model = CodeSnippet
        fields = ['code_snippet', 'language']  # Include the fields you want in your form
