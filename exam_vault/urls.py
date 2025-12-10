"""
URL configuration for exam_vault project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Customize admin site
admin.site.site_header = "DUTH VAULT - Admin Panel"
admin.site.site_title = "DUTH VAULT Admin"
admin.site.index_title = "Διαχείριση Συστήματος"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('exams.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

