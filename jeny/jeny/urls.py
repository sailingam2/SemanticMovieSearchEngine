from django.conf.urls import  include, url
from django.contrib import admin
from jenyapp.views import *
urlpatterns =[     # Examples:
    url(r'^$', home, name='home'),
    url(r'^register',register,name='register'),
    url(r'^signin',signin,name='signin'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^searchForm',searchForm,name="searchForm"),
    url(r'^movieinfo',getMovieInfo,name="movieinfo"),
    url(r'^actorinfo',getActorInfo,name="actorinfo"),
    url(r'^logout',logoutUser,name="logoutUser")
]
