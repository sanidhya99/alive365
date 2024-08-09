from django.contrib import admin
from django.urls import path,include
from authentication import urls as a
from doctors import urls as d
from users import urls as u
urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include(a)),
    path('doctor/', include(d)),
    path('user/', include(u)),
]