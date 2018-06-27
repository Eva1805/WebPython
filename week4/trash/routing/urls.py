from django.conf.urls import url
import views

urlpatterns = [
    url(r'^routing/simple_route/$', views.simple_route),
    url(r'^routing/slug_route/(?P<slug>[a-z0-9\-_]+)/$', views.slug_route),
    url(r'^routing/sum_route/(?P<a>[-]?[0-9]+)/(?P<b>[-]?[0-9]+)/$', views.sum_route),
    url(r'^routing/sum_get_method/$', views.sum_get_method),
    url(r'^routing/sum_post_method/$', views.sum_post_method),
    url(r'^template/echo/$', views.echo)

]
