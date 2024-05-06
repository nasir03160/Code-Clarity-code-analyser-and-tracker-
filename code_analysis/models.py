from django.db import models
from users.models import UserProfile 

class CodeSnippet(models.Model):
    code_snippet = models.TextField()
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    language = models.CharField(max_length=100)
    # submit_date = models.DateTimeField(auto_now_add=True)

class Analysis(models.Model):
    code_snippet = models.ForeignKey(CodeSnippet, on_delete=models.CASCADE)
    analysis_results = models.JSONField()
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class CustomAnalysis(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    code_snippet = models.ForeignKey(CodeSnippet, on_delete=models.CASCADE)
    formatted_code = models.TextField(blank=True, null=True)
    analysis_results1 = models.JSONField()
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

def get_dummy_analysis():
    dummy_analysis, created = Analysis.objects.get_or_create(
        code_snippet=None,  
        analysis_type='placeholder',  # Here's the issue
        analysis_results={} 
    )
    return dummy_analysis

    
class Feedback(models.Model):
    FEEDBACK_TYPES = (
        ('error', 'Error'),  # General errors (AST, Pylint)
        ('complexity', 'Complexity'), 
        ('explanation', 'Explanation'), 
    )
    analysis = models.ForeignKey(Analysis, on_delete=models.CASCADE, default=get_dummy_analysis)  # Link to Analysis
    feedback_type = models.CharField(max_length=20, choices=FEEDBACK_TYPES, default='explanation')
    message = models.TextField(default='Hello there seems to be an error analysisng your codeS')  # Store feedback content
    line_number = models.IntegerField(null=True, blank=True) # Optional, for line specific errors
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    

