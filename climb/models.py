from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone
from operator import itemgetter
class MainGoal(models.Model):
	id = models.AutoField(primary_key=True)
	user_id = models.ForeignKey(User)
	title = models.CharField(max_length=200)
	description = models.CharField(max_length=400)
	pub_date = models.DateTimeField('date published')
	deadline = models.DateTimeField(blank=True,null=True)
	if_done = models.BooleanField()
	done_date = models.DateTimeField(blank=True,null=True)

	def getgoals(self,user_id):
		return MainGoal.objects.filter(user_id = user_id).order_by('-pub_date')

class Task(models.Model):
	id = models.AutoField(primary_key=True)
	maingoal_id = models.ForeignKey(MainGoal)
	text = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published')
	deadline = models.DateTimeField(blank=True,null=True)
	if_done = models.BooleanField()
	done_date = models.DateTimeField(blank=True,null=True)
	def gettoday(self,user_id):
		todaytasks = []
		now = timezone.now()
		for i in MainGoal().getgoals(user_id):
			for j in Task.objects.filter(maingoal_id=i):
				if j.deadline:
					if (j.deadline.day == now.day and 
						j.deadline.month == now.month and
						j.deadline.year == now.year):
						todaytasks.append(j)
		return sorted(todaytasks,key=lambda x:x.deadline.time())
	def getgoaltasks(self,goal_id):
		pass
	def getalltasks(self,user_id):
		pass
class Daybook(models.Model):
	id = models.AutoField(primary_key=True)
	user_id = models.ForeignKey(User)

class DaybookCat(models.Model):
	id = models.AutoField(primary_key=True)
	text = models.CharField(max_length=100)

class DaybookPost(models.Model):
	id = models.AutoField(primary_key=True)
	daybook_id = models.ForeignKey(Daybook)
	pub_date = models.DateTimeField('date published')
	text = models.CharField(max_length=500)
	cathegory_id = models.ForeignKey(DaybookCat)
	def addpost(self,user_id,text):
		a = DaybookPost(daybook_id=Daybook.objects.get(user_id=user_id),
			pub_date=timezone.now(),
			text=text,
			cathegory_id=DaybookCat.objects.get(pk=1))
		a.save()
	def getposts(self,user_id):
		return DaybookPost.objects.filter(daybook_id=Daybook.objects.get(user_id=user_id),
			cathegory_id=DaybookCat.objects.get(pk=1)).order_by('-pub_date')
	def getactivities(self,user_id):
		return DaybookPost.objects.filter(daybook_id=Daybook.objects.get(user_id=user_id),
			cathegory_id=DaybookCat.objects.get(pk=2)).order_by('-pub_date')


class Feed(models.Model):
	id = models.AutoField(primary_key=True)
	user_id = models.ForeignKey(User)
	feed_id = models.ForeignKey(Daybook)

	def getposts(self,user_id):
		posts = [] 
		for i in Feed.objects.filter(user_id=user_id):
			for j in DaybookPost.objects.filter(daybook_id=i):
				posts.append(j)
		return posts

	def subscribe(self,user_id,feed_id):
		pass
class GoalCatList(models.Model):
	id = models.AutoField(primary_key=True)
	text = models.CharField(max_length=100)
	
class GoalCat(models.Model):
	id = models.AutoField(primary_key=True)
	goal_id = models.ForeignKey(MainGoal)
	cat_id = models.ForeignKey(GoalCatList)

class Activity(models.Model):
	id = models.AutoField(primary_key=True)
	user_id = models.ForeignKey(User)
	action = models.CharField(max_length=20)
	name_value = models.CharField(max_length=20)

class ActivityValue(models.Model):
	id = models.AutoField(primary_key=True)
	activity_id = models.ForeignKey(Activity)
	date = models.DateTimeField()
	value = models.IntegerField()

	def add_value(self,act_id,value):
		action = Activity.objects.get(id = act_id)
		myvalue = value
		a = ActivityValue(activity_id = action, date = timezone.now(),value=myvalue)
		a.save()

	def get_today_value(self,act_id,):
		values = ActivityValue.objects.filter(activity_id=act_id)
		final_value = 0
		if values:
			for i in values:
				if (i.date.day == timezone.now().day and 
					i.date.year == timezone.now().year and
					i.date.month == timezone.now().month):
					final_value = final_value + i.value

		return final_value	