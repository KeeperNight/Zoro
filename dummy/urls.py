from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', include('user.urls')),
    path('admin/', admin.site.urls),
    path('author/', include('author.urls')),
    path('book/', include('book.urls')),
    path('blog/', include('blog.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'user.views.handler404'
handler500 = 'user.views.handler500'
