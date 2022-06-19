from django.contrib import admin
from django.urls import path, include
from yesno_integration import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls', namespace='core')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns.append(
        path('__debug__', include(debug_toolbar.urls)),
    )
