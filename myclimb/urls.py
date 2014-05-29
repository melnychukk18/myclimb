from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'myclimb.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^$',include('climb.urls')),
    url(r'^', include('climb.urls', namespace="climb")),
    #url(r'^userpage/',include('climb.urls')),
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^register/',include('climb.urls')),
    #url(r'^register_success/',include('climb.urls'))
)
