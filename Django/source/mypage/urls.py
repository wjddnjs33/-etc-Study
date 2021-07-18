from django.conf.urls import url
from django.conf.urls import url as path
from server import views
from challenge import views as views2
from django.contrib import admin

app_name = 'server'
urlpatterns = [
	url(r'^admin', admin.site.urls),
	url(r'^signup', views.signup, name='signup'),
	url(r'^mypage', views.mypage),
	url(r'^login', views.login, name='login'),
	url(r'^logout', views.logout, name='logout'),
	url(r'^forgot', views.forgot, name='forgot'),
	url(r'^update', views.update, name='update'),
	url(r'^sqlcli', views.sqlcli, name='sqlcli'),
	url(r'^delete', views.delete, name='delete'),
	url(r'^admin_page', views.admin_page, name='admin'),
	path('challenge', views2.challenge),
	path('challenge/', views2.challenge),
	path('chall_1', views2.chall1, name='chall1'),
	path(r'activate/<str:uidb64>/<str:token>', views.activate, name="activate"),
	path(r'pw_activate/<str:uidb64>/<str:token>/', views.pw_activate, name="pw_activate"),
	path('', views.login, name='login')
] 