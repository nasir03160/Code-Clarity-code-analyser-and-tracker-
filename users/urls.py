from django.urls import path
from . import views
# from django.conf import settings
# from django.conf.urls.static import static
urlpatterns = [
    # path('',views.index,name='index'),
    path('', views.auth, name='auth'),  # Route to the single auth view
    # path('logout/', views.logout_view, name='logout'),  # Logout URL
]

    


# urlpatterns = urlpatterns+static(settings.MEDIA_URL,
# document_root=settings.MEDIA_ROOT)
