from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index,name = "index"),
    path('signup',views.signup,name = "signup"),
    path('logout',views.signout,name = "logout"),
    path('login',views.signin,name = "login"),
    path('share',views.share, name = "share"),
    path('list',views.listfiles,name = "list")
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)