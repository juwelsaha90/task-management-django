from django.shortcuts import render, redirect
from django.http import HttpResponse
from tasks.forms import TaskForm, TaskModelForm
from tasks.models import Employee, Task, TaskDetail, Project
from datetime import date
from django.db.models import Q, Count
from django.contrib import messages


def manager_dashboard(request):
    tasks = Task.objects.select_related("details").prefetch_related("assigned_to").all()
    # total_tasks = tasks.count()
    # pending_tasks = tasks.filter(status='PENDING').count()
    # in_progress_tasks = tasks.filter(status='IN_PROGRESS').count()
    # completed_tasks = tasks.filter(status='COMPLETED').count()

    counts = Task.objects.aggregate(
        total=Count('id'),
        pending=Count('id', filter=Q(status='PENDING')),
        in_progress=Count('id', filter=Q(status='IN_PROGRESS')),
        completed=Count('id', filter=Q(status='COMPLETED'))
    )

    context = {
        'tasks': tasks,
        'counts': counts
    }
    return render(request, 'dashboard/manager-dashboard.html', context)

def user_dashboard(request):
    return render(request, 'dashboard/user-dashboard.html')

def test(request):
    context = {
        'names': ['Mahmud', 'Ahmed', 'John'],
        'age': [20, 30, 40]
        
        
    }
    return render(request, 'test.html', context)

def create_task(request):
    
    form = TaskModelForm()
    
    if request.method == 'POST':
        form = TaskModelForm(request.POST)
        if form.is_valid():
            
            """ For django model form """
            form.save()

            return render(request, 'task_form.html', {'form': form, 'message': 'Task created successfully'})
            """ For django form """
           
            
    context = {"form": form}
    return render(request, 'task_form.html', context)


def delete_task(request, id):
    if request.method == 'POST':
        task = Task.objects.get(id=id)
        task.delete()
        messages.success(request,"Task deleted successfully")
        return redirect("manager-dashboard")

def view_task(request):
    
    tasks_count = Project.objects.annotate(num_tasks=Count('task'))
   
    return render(request, "show_task.html", {"tasks_count": tasks_count})

