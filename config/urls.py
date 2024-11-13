from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404, handler500


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("testlar.urls")),
    path("accounts/", include("accounts.urls")),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = 'django.views.defaults.page_not_found'
handler500 = 'django.views.defaults.server_error'