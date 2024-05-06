from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(CodeSnippet)
admin.site.register(Analysis)
admin.site.register(CustomAnalysis)
admin.site.register(Feedback)