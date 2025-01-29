from django.urls import path
from . import views
#from django.contrib.auth.views import logout_view
urlpatterns=[
    path('',views.home_view,name="home"),
    path("profile/",views.profile_view,name="profile"),
    path('register/',views.register_view,name="register"),
    path('prefernces/',views.preference_view,name="prefernces"),
    path('dashboard/',views.dashboard_view,name="dashboard"),
    path('bookmark/',views.bookmark_view),
    path('add_bookmark/',views.add_bookmark,name="add_bookmark"),
    path('login/',views.login_view,name="login"),
    path("logout/",views.logout_view,name='logout')
]