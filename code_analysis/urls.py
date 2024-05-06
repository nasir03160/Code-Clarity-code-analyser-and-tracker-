from django.urls import path,include
from . import views
urlpatterns = [
    path('codeclarity/',views.submit_code,name='codeclarity'),
    # path('analyze_code/', views.analyze_code, name='analyze_code'), 
   
]