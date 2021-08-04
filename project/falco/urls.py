from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path , include
from falco import settings, views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.index , name = "index"),
    path('information/', views.information , name="information"),

    path('accounts/', include('accounts.urls')),
    path('messenger/', include('messenger.urls')),
    
]
urlpatterns += static(settings.MEDIA_URL  ,  document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL ,  document_root=settings.STATIC_ROOT)

handler404 = "falco.views.error_404_view"
