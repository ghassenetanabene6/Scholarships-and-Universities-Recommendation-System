from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from appPCD.views import *
urlpatterns = [
    path('', index,name="index"),
    path('login/', loginUser,name="login"),
    path('signup/', signup,name="SignUp"),
    path('apropos/', apropos,name="Apropos"),
    path('historique/', historique,name="historique"),
    path('recommandation/', recom,name="Recommandation"),
    path('rec_sans_pref/', rec_sans,name="Rec_sans_pref"),
    path('rec_avec_pref/', rec_avec,name="Rec_avec_pref"),
    path('logout/', logoutUser,name="logout"),
    path('admin/', admin.site.urls),
    path('details/<int:id>', details,name="details"),
    path('histo/<int:classe>', histo,name="histo"),
    path('upload_csv/', scholarship_upload,name="upload_csv"),
]
