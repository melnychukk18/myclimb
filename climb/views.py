from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext, loader
from climb.models import MainGoal,Task,Daybook,DaybookCat,DaybookPost,Feed,Activity,ActivityValue
from django.core.context_processors import csrf
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
import datetime

#----- FORMS
class RegistrationForm(forms.Form):
    firstname = forms.CharField(max_length=100)
    lastname = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()
class LoginForm(forms.Form):
	#popover-placement="bottom" popover="On the Bottom!" popover-trigger="focus"
	username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','popover':'On the Bottom!',
		'popover-placement':'bottom','popover-trigger':'focus'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
class AddGoalForm(forms.Form):
	text = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Description'}))
	date = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'date'}))
	time = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'time'}))
class AddMainGoalForm(forms.Form):
	title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Title'}))
	text = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Description'}))

class AddToDaybook(forms.Form):
	text = forms.CharField(widget=forms.Textarea)

class AddActValue(forms.Form):
	value = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'act_value'}))
	act_id = forms.CharField(widget=forms.TextInput(attrs={'class': 'texthide'}))

#----- PAGES

#-----------------------------------NEW
#DEADLINES
def deadlines(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	else:
		return render(request,'climb/userpage/deadlines_list.html')

def todaytasks(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	else:
		if request.method != 'POST':
			form = AddActValue()
			tasks = Task().gettoday(request.user.pk)
			activities = Activity.objects.filter(user_id=request.user)
			final_act = []
			for i in activities:
				final_act.append([i,ActivityValue().get_today_value(i.pk)])

			return render(request,'climb/userpage/today_tasks.html',{
				'form':form,
				'tasks':tasks,
				'activities':final_act
				})
		else:
			form = AddActValue(request.POST)
			if form.is_valid():
				act_id = form.cleaned_data['act_id']
				value = form.cleaned_data['value']
				ActivityValue().add_value(act_id=int(act_id),value=value)
				return HttpResponseRedirect('/today')
			else:
				return HttpResponseRedirect('/deadlines')


def todaysecret(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	else:
		return render(request,'climb/userpage/today_secret.html')

def daybookposts(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	else:
		if request.method == 'POST':
			posts = DaybookPost().getposts(request.user)
			form = AddToDaybook(request.POST)
			if form.is_valid():
				text = form.cleaned_data['text']
				DaybookPost().addpost(user_id=request.user,
					text=text)
				return HttpResponseRedirect('/')
			else:
				return HttpResponseRedirect('/')
		else:
			posts = DaybookPost().getposts(request.user)
			form = AddToDaybook()
			return render(request,'climb/userpage/daybook_posts.html',{
				'posts':posts,
				'form':form
				})
			

def daybookactivities(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	else:
		posts = DaybookPost().getactivities(request.user.pk)
		return render(request,'climb/userpage/daybook_activities.html',{
			'posts':posts,
			})

def daybookadd(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	else:
		return render(request,'climb/userpage/daybook_add.html')

def statistics(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	else:
		return render(request,'climb/userpage/statistics.html')

def newgoalpage(request,goal_id):

	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	else:
		goal = MainGoal.objects.get(pk=goal_id)
		tasks = Task.objects.filter(maingoal_id = goal,if_done=False)
		return render(request,'climb/userpage/goalpage.html',{
			'goal':goal,
			'tasks':tasks
			})

def newaddtask(request,goal_id):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	elif MainGoal.objects.get(pk=goal_id).user_id != request.user:
		return HttpResponseRedirect('/')
	else:
		if request.method == 'POST':
			form = AddGoalForm(request.POST)
			if form.is_valid():
				text = form.cleaned_data['text']
				date = form.cleaned_data['date']
				time = form.cleaned_data['time']
				mytime = date+' '+time
				#WHAT_GOES_HERE = datetime.datetime.strptime(myStr, "%Y-%m-%d %H:%M")
				deadline = datetime.datetime.strptime(mytime, "%Y-%m-%d %H:%M")
				mytask = Task(maingoal_id=MainGoal.objects.get(pk=goal_id),text = text,
					pub_date = timezone.now(),deadline=deadline,if_done=False)

				mytask.save()
				return HttpResponseRedirect('/goal'+str(goal_id))
			else:
				return HttpResponseRedirect('')
		else:
			form = AddGoalForm();
			return render(request,'climb/userpage/task_add.html',{
				'form':form,
				})

def newdonetask(request,goal_id,task_id):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	else:
		task = Task.objects.get(pk=task_id)
		task.if_done = True
		task.save()
		return HttpResponseRedirect('/goal'+str(goal_id))

def today_done_task(request,task_id):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	else:
		task = Task.objects.get(pk=task_id)
		task.if_done = True
		task.save()
		return HttpResponseRedirect('/today')
#------------------------------------END NEW
#index/register
def index(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/id%s'%request.user.pk)
	if request.method == 'POST': 
		form = RegistrationForm(request.POST)
		if form.is_valid():
			firstname = form.cleaned_data['firstname']
			lastname = form.cleaned_data['lastname']
			password = form.cleaned_data['password']
			email = form.cleaned_data['email']
			username = form.cleaned_data['email']
			user = User.objects.create_user(username = username,
				first_name = firstname,
				last_name = lastname,
				email = email,
				password = password)
			user.save()
			daybook = Daybook(user_id = User.objects.filter(id = user.id)[0])
			daybook.save()
			user = authenticate(username=username,password=password)

			if user is not None:
				login(request, user)
				return HttpResponseRedirect('/id%s'%request.user.pk)
			

		return HttpResponseRedirect('/')
	else:
		form = RegistrationForm()
		
	return render(request,'climb/index.html',{
		'form': form,
		})

#loginpage
def loginpage(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/id%s'%request.user.pk)
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(username=username,password=password)
			if user is not None:
				login(request, user)
				return HttpResponseRedirect('/today')
	else:
		form = LoginForm()
		return render(request,'climb/loginpage.html',{
		'form': form,
		})

#userpage	
def user_goal_list(request,user_id):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	else:
		if request.method != 'POST':
			main_goal_list = []
			for i in MainGoal.objects.filter(user_id=user_id):
				main_goal_list.append([i,Task.objects.filter(
					maingoal_id=i.id,if_done=False).count])
			user = User.objects.get(pk = user_id)
			form = AddMainGoalForm()
			return render(request,'climb/userpage/goal_list.html',{
				'main_goal_list':main_goal_list,
				'username':User.objects.get(pk = user_id),
				'firstname':user.first_name,
				'lastname':user.last_name,
				'user':User.objects.get(pk=user_id),
				'form': form,
				})
		else:
			form = AddMainGoalForm(request.POST)
			if form.is_valid():
				goaltitle = form.cleaned_data['title']
				goaltext = form.cleaned_data['text']
				g = MainGoal(user_id=User.objects.get(pk=request.user.pk),
					title=goaltitle,description=goaltext,pub_date = timezone.now(),
					if_done=False)
				g.save()
				daytext = 'added new goal: ('+str(goaltitle)+')'
				d = DaybookPost(daybook_id=Daybook.objects.get(user_id=request.user),
					text = daytext,pub_date = timezone.now(),cathegory_id=DaybookCat.objects.get(id=2))
				d.save()
				return HttpResponseRedirect('/id%s'%request.user.pk)
			else:
				return HttpResponseRedirect('/id%s'%request.user.pk)

#addgoalpage
def addgoal(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	else:
		if request.method == 'POST':
			form = AddMainGoalForm(request.POST)
			if form.is_valid():
				goaltitle = form.cleaned_data['title']
				goaltext = form.cleaned_data['text']
				g = MainGoal(user_id=User.objects.get(pk=request.user.pk),
					title=goaltitle,description=goaltext,pub_date = timezone.now(),
					if_done=False)
				g.save()
				daytext = 'added new goal: ('+str(goaltitle)+')'
				d = DaybookPost(daybook_id=Daybook.objects.get(user_id=request.user),
					text = daytext,pub_date = timezone.now(),cathegory_id=DaybookCat.objects.get(id=2))
				d.save()
				return HttpResponseRedirect('/id%s'%request.user.pk)
		else:
			form = AddMainGoalForm()
			return render(request, 'climb/userpage/goal_add.html',{
				'form': form,
				})

#addtaskpage
def addtask(request,user_id,goal_id):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	else:
		if request.method == 'POST':
			form = AddGoalForm(request.POST)
			if form.is_valid():
				goaltext = form.cleaned_data['text']
				g = Task(
					maingoal_id=MainGoal.objects.get(pk=goal_id),
					text=goaltext,
					pub_date= timezone.now(),
					if_done=False)
				g.save()
				return HttpResponseRedirect('/id%s'%request.user.pk)
		else:
			form = AddGoalForm()
			return render(request, 'climb/addgoal.html',{
				'form': form,
				'username': request.user
				})

#taslist
def tasklist(request,user_id,goal_id):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	else:
		goal_list = Task.objects.filter(
			maingoal_id=goal_id,if_done = False)
		return render(request,'climb/tasklist.html',{
			'goal_list':goal_list,
			'username': request.user
			})

#donetask
def done_task(request,user_id,goal_id,task_id):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	else:
		s_goal = Task.objects.filter(id=task_id).update(if_done=True)
		
		return HttpResponseRedirect('/id'+user_id+'/goalslist/'+goal_id)

#logout
def logoutpage(request):
	logout(request)
	return HttpResponseRedirect('/login')


#daybook
def daybook(request,user_id):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	else:
		if request.method == 'POST':
			form = AddToDaybook(request.POST)
			if form.is_valid():
				t = form.cleaned_data['text']

				d = Daybook(user_id=User.objects.get(pk=request.user.pk),
					text = t,pub_date = timezone.now())
				d.save()
				return HttpResponseRedirect('/id'+user_id+'/daybook')
			else:
				return HttpResponseRedirect('/id'+user_id+'/daybook')
		else:
			form = AddToDaybook()
		posts = Daybook.objects.filter(user_id=user_id)
		return render(request,'climb/daybook.html',{
			'posts':posts,
			'form':form
			})
def mypage(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	else:
		return HttpResponseRedirect('/id'+str(request.user.pk))

def full_tasklist(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	else:
		user = request.user.pk
		tasklist = Task.objects.filter(maingoal_id = MainGoal.objects.filter(user_id=user),
			if_done=False)
		return render(request, 'climb/fulltasklist.html',
			{
				'tasklist':tasklist
			})

def myfeed(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	else:
		user = request.user.pk
		posts = Feed().getposts(user)
		return render(request,'climb/tasklist.html',{
			'goal_list':posts,
			'username': request.user
			})




