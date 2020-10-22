from django.apps import apps
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from customs.views import signup_view, activation_sent_view, catagories_product,check_pincode



urlpatterns = [
    path('spadmin/', admin.site.urls),
    path('account/register/', signup_view),
    path('account/verificaation/<uidb64>', activation_sent_view),
    path('catalogue/', catagories_product),
    path('', include(apps.get_app_config('oscar').urls[0])),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)