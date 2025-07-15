from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cv/', include('cv.urls')),
    path('api/auth/', include('authentication.urls')),
    path('', TemplateView.as_view(template_name='cv/index.html'), name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)