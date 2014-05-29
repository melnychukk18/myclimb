from django.conf.urls import patterns,url
from climb import views

urlpatterns = patterns('',
	url(r'^$',views.index, name='index'),
	url(r'^login/$',views.loginpage, name='mylog'),
	url(r'^logout/$',views.logoutpage, name='logout'),
	url(r'^mypage/$',views.mypage, name='logout'),
	url(r'^tasklist/$',views.full_tasklist,name = 'full_tasklist'),
	url(r'^feed/$',views.myfeed,name = 'feed'),
	url(r'^addgoal/$',views.addgoal, name='user'),
	#---------------------------------------NEW
	url(r'^deadlines/$',views.deadlines, name='user'),

	url(r'^today/$',views.todaytasks, name='user'),
	url(r'^today_secret/$',views.todaysecret, name='user'),

	url(r'^daybook_posts/$',views.daybookposts, name='user'),
	url(r'^daybook_activities/$',views.daybookactivities, name='user'),
	url(r'^daybook_add/$',views.daybookadd, name='user'),

	url(r'^statistics/$',views.statistics, name='user'),

	url(r'^goal(?P<goal_id>\d+)/$',views.newgoalpage,name='goalpage'),
	url(r'^goal(?P<goal_id>\d+)/add$',views.newaddtask,name='goalpage'),
	url(r'^goal(?P<goal_id>\d+)/done(?P<task_id>\d+)/$',views.newdonetask,name='goalpage'),
	url(r'^tdone(?P<task_id>\d+)/$',views.today_done_task,name='goalpage'),
	#---------------------------------------ENDNEW
	#--------------
	url(r'^id(?P<user_id>\d+)/$',views.user_goal_list, name='user'),
	
	url(r'^id(?P<user_id>\d+)/addtomain/(?P<goal_id>\d+)/$',views.addtask, name='user'),
	url(r'^id(?P<user_id>\d+)/goalslist/(?P<goal_id>\d+)/$',views.tasklist, name='user'),
	url(r'^id(?P<user_id>\d+)/goalslist/(?P<goal_id>\d+)/done/(?P<task_id>\d+)$',
		views.done_task, name='user'),
	url(r'^id(?P<user_id>\d+)/daybook/$',views.daybook,name='daybook')
)