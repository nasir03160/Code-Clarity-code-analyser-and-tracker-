from django.urls import path,include
from . import views
from users.views import auth
from code_analysis import views as analysis_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',auth,name='auth'),
    # path('codeclarity/',analysis_views.submit_code,name='codeclarity')
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
