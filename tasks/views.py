from django.shortcuts import render, redirect
from django.http import HttpResponse
from tasks.forms import TaskForm, TaskModelForm
from tasks.models import Employee, Task, TaskDetail, Project
from datetime import date
from django.db.models import Q, Count
from django.contrib import messages


def manager_dashboard(request):
    type = request.GET.get('type','all')
    
   

    counts = Task.objects.aggregate(
        total=Count('id'),
        pending=Count('id', filter=Q(status='PENDING')),
        in_progress=Count('id', filter=Q(status='IN_PROGRESS')),
        completed=Count('id', filter=Q(status='COMPLETED'))
    )

    base_query = Task.objects.select_related("details").prefetch_related("assigned_to")
    if type == 'pending':
        tasks = base_query.filter(status='PENDING')
    elif type == 'in_progress':
        tasks = base_query.filter(status='IN_PROGRESS')
    elif type == 'completed':
        tasks = base_query.filter(status='COMPLETED')
    else:
        tasks = base_query.all()



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

