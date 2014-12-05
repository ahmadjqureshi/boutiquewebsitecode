from django.conf.urls import patterns, include, url
from django.contrib import admin
from boutique_app import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'boutique.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),
    url(r'^hello.jpt/$', views.hello),
    url(r'^index/', views.index),
    url(r'^add_product/', views.add_product_step1_form),
    url(r'^testajax/', views.ajaxtest),
    url(r'^uploadimage/', views.imageupload),
    url(r'^deleteimage/', views.deleteimage),
    url(r'^viewproducts/$', views.viewproducts),
    url(r'^productdetail/$', views.productdetail),
    url(r'^loginform/', views.loginform ),
    url(r'^loginprocess/', views.loginprocess ),
    url(r'^mainpage/', views.mainpage ),
    url(r'^logout/', views.logoutpage ),
    url(r'^contact/', views.contact ),
)

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
