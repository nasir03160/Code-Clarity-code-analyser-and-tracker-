from django.contrib import admin
from django.urls import path,include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('frontend.urls')),
    path('',include('code_analysis.urls')),
    path('',include('users.urls')),    
    # path('')
]
