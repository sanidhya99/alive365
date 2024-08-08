from django.contrib import admin
from django.urls import path,include
from authentication import urls as a
urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include(a)),
    # path('shop/', include(d)),

]