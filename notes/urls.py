from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',views.home_page, name='home_page'),
    url(r'^upload/',views.upload_page, name='upload_page'),
    url(r'^api/upload/', views.upload_api, name='api_upload'),
    url(r'^api/addcomment/', views.addcomment_api, name='addcomment_api'),
    url(r'^search/$', views.search, name='search'),
    url(r'^about/', views.about, name='about'),
    
    path('notes/<int:note_index>/', views.detail,name='detail'),
    path('tag/<str:tag>', views.tag_query, name='tag_query'),
    path('help/', views.help, name='help'),
    path('help/<str:help_topic>', views.help_detail, name='help_detail'),
    path('delete/<int:note_id>/', views.delete, name='delete'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
