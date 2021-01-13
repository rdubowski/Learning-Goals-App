from django.shortcuts import render, redirect, get_object_or_404
from .models import LearningGoal, SingleTask
from django.db.models import Prefetch, Count
from django.contrib import messages
from .forms import CreateUserForm, CreateGoalForm, SingleTaskForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import View, TemplateView
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.contrib.auth.mixins import LoginRequiredMixin


def welcome_screen(request):
    context = {}
    return render(request, 'to_do_manager/hello_screen.html', context)


def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            messages.success(request, 'Account was created for ' + username)

            return redirect('login')

    context = {'form': form}
    return render(request, 'to_do_manager/register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.info(request, 'Username OR password is incorrect')
        context = {}
        return render(request, 'to_do_manager/login.html', context)

def logoutPage(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def dashboard(request):
    template_name = 'to_do_manager/dashboard.html'
    LearningGoals = request.user.learninggoal_set.prefetch_related(
         Prefetch('tasks', queryset=SingleTask.objects.filter(completed=False))).annotate(
         counter=Count('tasks')).order_by('-updated_at')
    context = {'LearningGoals': LearningGoals}
    return render(request, template_name, context)


@login_required(login_url='login')
def create_goal(request):
    if request.method == 'POST':
        form = CreateGoalForm(request.POST)
        user = request.user
        if form.is_valid():
            new_learning_goal = LearningGoal()
            new_learning_goal.name = form.cleaned_data['name']
            new_learning_goal.user = user
            new_learning_goal.save()
            return redirect('dashboard')
    form = CreateGoalForm()
    context = {'form' :form}
    return render(request, 'single_goal/create_goal.html', context)

@login_required(login_url='login')
def deleteGoal(request, pk):
    goal = LearningGoal.objects.get(id=pk)
    if request.method == "POST":
        goal.delete()
        return redirect('dashboard')
    context = {'goal': goal}
    return render(request, 'single_goal/delete_goal.html', context)


@login_required(login_url='login')
def changeGoalName(request, pk):
    learning_goal = get_object_or_404(LearningGoal, id=pk)
    form = CreateGoalForm(request.POST or None, instance=learning_goal)
    if form.is_valid():
        form.save()
        return redirect('dashboard')
    context = {'form' :form, 'learninggoal': learning_goal}
    return render(request, 'single_goal/change_goal_name.html', context)





# def LearningGoalTasks(request, id):
#     tasks = LearningGoal.objects.get(id=id).tasks.all()
#     form = CreateSingleTask()
#     context = {'tasks': tasks, 'form': form}
#     return render(request, 'single_goal/create_tasks.html', context)

# class TaskList(LoginRequiredMixin, TemplateView):
#     def get(self, request, *args, **kwargs):
#         form = SingleTaskForm()
#         tasks = LearningGoal.objects.get(id=2).tasks.all()
#         context = {'form' : form, 'tasks' : tasks}
#         return render (request, 'single_goal/create_tasks.html', context)

#     def post(self,request):
#         form = SingleTaskForm(request.POST)
#         if form.is_valid():
#             new_task = SingleTask()
#             new_task.text = form.cleaned_data['text']
#             new_task.learninggoal = LearningGoal.objects.get(id=1)
#             new_task.save()
#             return JsonResponse({'task': model_to_dict(new_task)}, status=200)
#         else:
#             return redirect('task_list_url')


@login_required(login_url='login')
def learningGoalTasks(request, pk):
    learning_goal = LearningGoal.objects.get(id=pk)
    if request.method == "POST":
        form = SingleTaskForm(request.POST)
        if form.is_valid():
            new_task = SingleTask()
            new_task.text = form.cleaned_data['text']
            new_task.learninggoal = learning_goal
            new_task.save()
            return JsonResponse({'task': model_to_dict(new_task)}, status=200)
        else:
            return redirect('task_list_url')
    else:
        form = SingleTaskForm()
        tasks = learning_goal.tasks.all()
        context = {'form' : form, 'tasks' : tasks, 'learning_goal': learning_goal}
        return render (request, 'single_goal/create_tasks.html', context)




@login_required(login_url='login')
def TaskComplete(request, id):
   if request.method == "POST":
        task = SingleTask.objects.get(id=id)
        task.completed = True
        task.save()
        return JsonResponse({'task': model_to_dict(task)}, status=200)


@login_required(login_url='login')
def TaskDelete(request, id):
    if request.method == "POST":
        task = SingleTask.objects.get(id=id)
        task.delete()
        return JsonResponse({'result': 'ok'}, status=200)

