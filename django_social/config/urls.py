
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    # path("chat/", include("chat.urls")),
    path("", include('main.urls')),
    path('chat/', include('chat.urls')),
    
    path('api-auth/', include('rest_framework.urls')),

    path('api-main/', include('api.api_main.urls'))
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


