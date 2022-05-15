import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),
    path("admin/", admin.site.urls),
    path("", include("budget.urls", namespace="budget")),  
    path('api-auth/', include('rest_framework.urls')) ,
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Budget and Accounting System"
admin.site.index_title = "User Admin"